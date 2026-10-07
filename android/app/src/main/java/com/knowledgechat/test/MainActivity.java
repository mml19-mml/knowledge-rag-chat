package com.knowledgechat.test;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;
import org.json.JSONObject;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Test-only shell. UI is packaged locally; real RAG requests stay on the configured backend. */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int EXPORT_JSON = 1401;
    private final ExecutorService requests = Executors.newFixedThreadPool(2);
    private WebView webView;
    private FrameLayout root;
    private String exportContent;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(250,248,252));
        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(250,248,252));
        root.addView(webView, new FrameLayout.LayoutParams(-1,-1));
        setContentView(root);
        if (Build.VERSION.SDK_INT >= 30) {
            getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((v, insets) -> {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                android.graphics.Insets ime = insets.getInsets(WindowInsets.Type.ime());
                v.setPadding(bars.left,bars.top,bars.right,Math.max(bars.bottom,ime.bottom));
                return WindowInsets.CONSUMED;
            });
        }
        getWindow().setStatusBarColor(Color.TRANSPARENT);
        getWindow().setNavigationBarColor(Color.TRANSPARENT);
        if (Build.VERSION.SDK_INT >= 29) getWindow().setNavigationBarContrastEnforced(false);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSupportMultipleWindows(false);
        webView.addJavascriptInterface(new NativeBridge(),"KnowledgeNative");
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG);
        webView.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request) {
                Uri uri=request.getUrl();
                if (!"https".equals(uri.getScheme()) || !HOST.equals(uri.getHost())) return denied();
                String relative=uri.getPath();
                if (relative==null || relative.contains("..") || relative.contains("\\")) return denied();
                if (relative.equals("/")) relative="/index.html";
                try {
                    InputStream stream=getAssets().open("public"+relative);
                    String type=relative.endsWith(".html")?"text/html":relative.endsWith(".js")?"text/javascript":relative.endsWith(".css")?"text/css":relative.endsWith(".png")?"image/png":relative.endsWith(".ttf")?"font/ttf":"application/octet-stream";
                    HashMap<String,String> headers=new HashMap<>();
                    headers.put("Cache-Control","no-store");
                    headers.put("X-Content-Type-Options","nosniff");
                    return new WebResourceResponse(type,"UTF-8",200,"OK",headers,stream);
                } catch(Exception ex) { return denied(); }
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request) {
                Uri uri=request.getUrl();
                // Only trusted bundled pages may keep access to the native bridge.
                return !("https".equals(uri.getScheme()) && HOST.equals(uri.getHost()));
            }
        });
        webView.loadUrl("https://"+HOST+"/");
    }
    private WebResourceResponse denied() {
        return new WebResourceResponse("text/plain","UTF-8",404,"Not Found",new HashMap<>(),new ByteArrayInputStream(new byte[0]));
    }
    @Override public void onBackPressed() {
        webView.evaluateJavascript("Boolean(document.querySelector('dialog[open]'))",result -> {
            if ("true".equals(result)) webView.evaluateJavascript("document.querySelector('dialog[open]').close()",null);
            else if (webView.canGoBack()) webView.goBack();
            else super.onBackPressed();
        });
    }
    private void reply(String id, JSONObject response) {
        runOnUiThread(() -> {if(!isFinishing()&&!isDestroyed()) webView.evaluateJavascript("window.__nativeReply("+JSONObject.quote(id)+","+response+")",null);});
    }
    private JSONObject failure(String message) {
        JSONObject result=new JSONObject();try{result.put("ok",false);result.put("error",message);}catch(Exception ignored){}return result;
    }
    private void nativeRequest(String id,String base,String operation,String payload) {
        requests.execute(() -> {
            HttpURLConnection connection=null;
            try {
                URL origin=new URL(base);
                if (!(origin.getProtocol().equals("http")||origin.getProtocol().equals("https")) || origin.getHost().isEmpty() || origin.getUserInfo()!=null || origin.getQuery()!=null || origin.getRef()!=null) {reply(id,failure("请输入有效的 HTTP 或 HTTPS 服务地址。"));return;}
                String route=operation.equals("ask")?"/api/rag/ask":operation.equals("health")?"/api/health":operation.equals("health-legacy")?"/health":null;
                if(route==null || payload.length()>16000) {reply(id,failure("无效请求。"));return;}
                URL target=new URL(base.replaceAll("/+$","")+route);
                connection=(HttpURLConnection)target.openConnection();
                connection.setInstanceFollowRedirects(false);
                connection.setConnectTimeout(12000);
                connection.setReadTimeout(operation.equals("ask")?120000:12000);
                connection.setRequestProperty("Accept","application/json");
                if(operation.equals("ask")) {
                    connection.setRequestMethod("POST");
                    connection.setDoOutput(true);
                    connection.setRequestProperty("Content-Type","application/json; charset=utf-8");
                    try(OutputStream out=connection.getOutputStream()){out.write(payload.getBytes(StandardCharsets.UTF_8));}
                }
                int status=connection.getResponseCode();
                InputStream raw=status>=400?connection.getErrorStream():connection.getInputStream();
                ByteArrayOutputStream bytes=new ByteArrayOutputStream();
                if(raw!=null)try(InputStream in=raw){byte[] chunk=new byte[8192];int count;while((count=in.read(chunk))!=-1){if(bytes.size()+count>2*1024*1024)throw new Exception("服务返回内容过大");bytes.write(chunk,0,count);}}
                JSONObject result=new JSONObject();result.put("ok",status>=200&&status<300);result.put("status",status);result.put("body",bytes.toString(StandardCharsets.UTF_8.name()));reply(id,result);
            }catch(Exception ex){reply(id,failure("连接失败，请检查服务地址、网络及电脑上的 RAG 服务。"));}
            finally{if(connection!=null)connection.disconnect();}
        });
    }
    public class NativeBridge {
        @JavascriptInterface public void request(String id,String base,String operation,String payload){nativeRequest(id,base,operation,payload);}
        @JavascriptInterface public void copyText(String text){runOnUiThread(()->{ClipboardManager clipboard=(ClipboardManager)getSystemService(CLIPBOARD_SERVICE);clipboard.setPrimaryClip(ClipData.newPlainText("Knowledge Chat",text));});}
        @JavascriptInterface public void setTheme(String value){runOnUiThread(()->{
            boolean dark="dark".equals(value);int color=dark?Color.rgb(9,9,9):Color.rgb(250,248,252);root.setBackgroundColor(color);webView.setBackgroundColor(color);
            if(Build.VERSION.SDK_INT>=30){WindowInsetsController c=getWindow().getInsetsController();if(c!=null){int flags=WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS;c.setSystemBarsAppearance(dark?0:flags,flags);}}
            else getWindow().getDecorView().setSystemUiVisibility(dark?0:View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR|View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        });}
        @JavascriptInterface public void exportJson(String name,String content){if(content.length()>5*1024*1024)return;runOnUiThread(()->{
            exportContent=content;
            Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("application/json");intent.putExtra(Intent.EXTRA_TITLE,name.replaceAll("[^a-zA-Z0-9._-]","_"));
            try{startActivityForResult(intent,EXPORT_JSON);}catch(Exception ex){exportContent=null;Toast.makeText(MainActivity.this,"没有可用的文件保存程序",Toast.LENGTH_SHORT).show();}
        });}
    }
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){
        super.onActivityResult(requestCode,resultCode,data);
        if(requestCode==EXPORT_JSON){if(resultCode==RESULT_OK&&data!=null&&data.getData()!=null&&exportContent!=null){try(OutputStream out=getContentResolver().openOutputStream(data.getData())){out.write(exportContent.getBytes(StandardCharsets.UTF_8));Toast.makeText(this,"对话已导出",Toast.LENGTH_SHORT).show();}catch(Exception ex){Toast.makeText(this,"保存失败，请重试",Toast.LENGTH_SHORT).show();}}exportContent=null;}
    }
    @Override protected void onDestroy(){requests.shutdownNow();if(webView!=null){webView.removeJavascriptInterface("KnowledgeNative");webView.destroy();}super.onDestroy();}
}
