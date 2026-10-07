# Knowledge Chat Android

Knowledge Chat 的安卓访客客户端，作为主仓库的 `android/` 子目录维护。复用现有 RAG 后端和知识库；资料上传与管理仍在独立的网页管理端完成。

这是用于安装测试的原型：本地 WebView 加载随 APK 打包的 HTML、CSS 和 JavaScript，Java 层提供网络请求、复制、文件导出、系统返回与日夜主题适配。默认使用离线演示，不自动连接任何个人服务器。

## 功能

- 提问、继续提问、来源引用预览。
- 本机聊天历史、搜索、归档、恢复和 JSON 导出。
- 浅色与深色主题、本机显示名称。
- 在 Setting 中配置 RAG 根地址并检测连接。
- 示例回答和真实服务回答分别标注；后端返回占位内容时明确提示。

离线模式使用预置示例文本，没有内置模型或真实知识库。启用 RAG 模式后，请求由现有后端处理，APK 内不存放模型 API 密钥或管理员密钥。

## 与网页项目的关系

```text
knowledge-rag-chat/
├── backend/          # 共用的 RAG 后端
├── frontend/         # 网页问答与管理界面
├── android/          # 本目录：安卓访客客户端
├── scripts/
├── docker-compose.yml
└── README.md
```

本目录独立构建，不需要替换主仓库现有的 `backend/` 或 `frontend/`。手机和网页通过网络访问同一套资料与问答服务。

## 构建

需要 Android Studio 或等效的 Android 工具链：JDK 17+、Android SDK Platform 36、Build Tools 35.0.0。项目使用 Gradle 8.13 与 Android Gradle Plugin 8.13.0；Gradle Wrapper 已附带，首次使用会下载对应 Gradle 发行包。

### Windows

打开 PowerShell，进入本目录并运行：

```powershell
.\Build-APK.ps1
```

脚本从环境变量或常见安装位置查找 SDK 和 Java。使用自定义安装位置时，可传入 `-SdkPath` 和 `-JdkPath`。生成的 `local.properties` 仅供本机使用，已被 `.gitignore` 排除。

也可以在 Android Studio 中打开本目录，由 IDE 配置 SDK 后构建 Debug APK。macOS/Linux 可配置好 SDK 和 JAVA_HOME 后使用 `sh ./gradlew assembleDebug`。

生成文件：

```text
app/build/outputs/apk/debug/app-debug.apk
```

最低 Android 8.0。Web 界面使用现代 Android System WebView 功能，建议使用已更新的系统 WebView。无需上架或注册开发者账户即可自行安装测试。

## 连接同一套 RAG

在手机 Setting → 问答连接中，选择“连接 RAG 服务”，填写可从手机访问的**根地址**，点击“测试连接”并保存。不要在地址后重复添加 `/api`。

主项目默认 Docker 配置中，网页服务的 `15173` 端口会将 `/api/*` 转发至同一个后端，因此也可以作为手机的 API 入口。实际地址取决于部署方式、电脑局域网 IP 或公开域名，源码中没有预填实际服务器地址。

客户端使用：

- `GET /api/health`：连接检查，仅在 HTTP 404 时兼容 `GET /health`。
- `POST /api/rag/ask`：请求体包含 `question`、`limit` 和 `document_id`，接收 `answer`、`sources` 与 `is_placeholder`。

手机上的 `localhost` 指手机本身。局域网测试需要电脑后端处于运行状态、网络可互通；公网部署建议使用 HTTPS。健康检查通过只代表服务有响应，完整问答还需后端有资料及有效模型配置。

## 签名与隐私

- 本仓库不包含 `.keystore`、`.jks` 或私有签名配置。Debug 构建使用本机自动生成的调试签名。
- 保留你已有测试 APK 的原签名私钥于私人目录，不要提交。换一个签名构建出的同包名 APK 不能覆盖安装旧签名版本。
- 若为了测试另一签名版本而卸载旧版，先导出需要保留的聊天记录；卸载会清除原应用的数据与设置。
- 模型密钥、管理员密钥留在后端；不要写入 Java、网页脚本或 Gradle。
- 聊天记录、显示名称、主题及连接地址保存在应用自己的本机存储中，源码只含明确标注的示例。
- `.gitignore` 排除构建产物、本机配置、签名文件与常见私有数据。公开前仍需检查实际上传列表；忽略规则不能移除已经公开的 Git 历史或其他压缩包中的内容。

此版本是测试原型，允许局域网 HTTP，Debug 构建启用 WebView 调试。面向长期公开运营时需要另行配置发布签名、HTTPS、服务认证和访问限制。

## 验证范围

此公开副本仅调整构建、签名分离和文档，沿用 0.1.1 的访客界面与连接逻辑。原测试 APK 的用户反馈确认可以安装并使用离线演示；真实 RAG 的运行地址和知识库状态由部署者配置。不同签名构建不表示已在所有安卓机型上验证。

第三方资源说明见 `THIRD_PARTY_NOTICES.md`。
