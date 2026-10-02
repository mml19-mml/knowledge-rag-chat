# Knowledge Chat

一个轻量的知识库问答网站：管理员预先导入 PDF，访客直接提问，回答附文件名及页码引用。

向量化默认在本地 CPU 上运行；回答生成使用 DeepSeek 或其他 OpenAI-compatible 聊天模型。无需额外申请 Embedding API Key。

## 功能

- 公开问答首页，无访客注册或登录。
- 独立 `/admin` 页面，支持 PDF 上传、状态查看、删除和向量索引重建。
- PDF 解析、分块、本地多语言 Embedding、Qdrant 向量检索与 BM25 混合检索。
- 回答展示资料来源；检索无结果或模型服务不可用时显示对应提示。
- 管理接口校验管理员凭证，凭证仅保存在管理页面内存中。
- Docker Compose 启动，Nginx 同源代理前端与 API。

## 架构

```text
管理员上传 PDF → 解析与分块 → PostgreSQL 保存文本
                          → 本地 Embedding → Qdrant 保存向量

访客提问 → 混合检索 → 相关资料 + 问题 → 聊天模型 → 回答与引用
```

前端：Vue 3、TypeScript、Vite。后端：FastAPI、SQLAlchemy、Alembic。
本地模型：`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`，384 维，CPU 推理。

## 快速开始

需要 Docker Desktop（Linux 容器）及 Docker Compose v2。进入包含 `docker-compose.yml` 的项目根目录。

### 1. 创建本地配置

PowerShell：

```powershell
Copy-Item backend/.env.example backend/.env
notepad backend/.env
```

macOS / Linux：

```bash
cp backend/.env.example backend/.env
```

填写以下值，真实凭证只保存在自己的 `.env` 中：

| 配置 | 说明 |
| --- | --- |
| `ADMIN_API_KEY` | 至少 32 字符的随机管理员凭证，与聊天模型 Key 不同 |
| `OPENAI_API_KEY` | 聊天模型供应商的 API Key |
| `OPENAI_BASE_URL` | 聊天 API 地址；DeepSeek 使用 `https://api.deepseek.com` |
| `OPENAI_MODEL` | 供应商当前支持的完整模型 ID，不能只写供应商名称 |

有 Python 时，可生成管理员凭证：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

将输出保存到 `ADMIN_API_KEY`。本地向量配置保持默认，`EMBEDDING_API_KEY` 留空。

### 2. 启动并准备模型

```bash
docker compose up -d --build
docker compose exec backend python scripts/prepare_local_model.py
```

首次构建下载依赖；首次准备模型下载公开模型文件。看到 `Local model ready` 才表示模型加载与向量生成成功。模型缓存在 Docker 的 `embedding_models` 卷中。下载需要网络，后续可复用缓存；缓存完整后可设置 `EMBEDDING_LOCAL_FILES_ONLY=true` 并重新创建后端以仅从缓存加载。

### 3. 上传和提问

- 管理页面：<http://localhost:15173/admin>
- 本地问答：<http://localhost:15173/>

进入管理页面，输入管理员凭证，上传一份有可提取文字的 PDF。检查片段数大于 0，且没有向量索引警告，再提问并核对引用。

默认宿主机端口为前端 `15173`、后端 `18000`、数据库 `15432`、Qdrant `16333`。后三项只绑定本机回环地址。端口冲突时仅修改 Compose `ports` 中左侧的宿主机端口，保持容器内部端口和服务连接地址不变。

## 管理资料与更新配置

- 添加资料：在 `/admin` 上传 PDF。
- 替换资料：删除旧文件后再上传新版，同名上传不自动覆盖。
- 索引警告：确认模型缓存和 Qdrant 可用，然后点击“重建索引”。文本解析完成不等于向量索引成功。
- 更换向量模型：使用新的 Qdrant collection 和匹配维度，对已有文件重新索引，不能混用不同模型的向量。
- 修改 `backend/.env` 后：

```bash
docker compose up -d --no-deps --force-recreate backend
```

PDF 原文件在 `backend/uploads`；结构化文本、向量和模型缓存分别保存在 Docker 数据卷中。备份应覆盖这些数据，不只是源码文件夹。`docker compose down` 保留数据卷；`docker compose down -v` 会删除数据卷，请勿用作日常重启方式。

## 临时体验链接

在本地问答正常运行后，Windows / macOS Docker Desktop 用户可运行：

```bash
docker run --rm -it cloudflare/cloudflared:latest tunnel --url http://host.docker.internal:15173
```

将终端新生成的 HTTPS 地址发给体验者。需要保持电脑、Docker 和隧道运行；这是临时测试入口，不能保证长期可用。该方式转发整个站点，`/admin` 并未被网络规则隐藏，管理操作仍受凭证保护。不要分享管理员凭证。

GitHub Public 仓库用于公开源码，不会自动运行这个 Python、数据库和模型服务组合；GitHub Pages 也不能直接托管完整后端。

## 数据与安全边界

- **本地 Embedding 不等于完全离线问答**：检索出的文本会发送给所配置的外部聊天模型。仅导入允许这样使用的资料。
- 访客可以通过问答获取知识库中的内容，知识库应视为对体验者可见。
- 聊天记录仅保存在页面内存中，每个问题独立检索，不支持跨轮记忆。
- PDF 正文 OCR、Word 导入和精细的文档访问权限不在当前功能范围内。
- 回答按纯文本显示，可能保留 Markdown / LaTeX 标记；引用和提示词不保证回答绝对正确。
- 示例数据库使用 `postgres` 本地开发凭证，它不是线上秘密。正式部署前配置独立数据库凭证、HTTPS、访问控制和适合实际代理链的限流，不要直接公开数据库端口。
- 只读公开源码不会泄露自己本机的 `.env`，但上传含 `.env` 的 ZIP、备份或历史提交会泄露。

## 开发与测试

Python 3.11/3.12、Node.js 22。Docker 数据服务的宿主机连接端口与模板一致：PostgreSQL `15432`，Qdrant `16333`；Compose 会为容器覆盖成内部服务地址。

```bash
docker compose up -d postgres qdrant
cd backend
python -m venv .venv
# 激活虚拟环境后执行；Windows 也可直接使用 .venv/Scripts/python
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-test.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

另一终端：

```bash
cd frontend
npm ci
npm run dev
```

开发前端默认端口 `5173`，代理到本机后端 `8000`；与 Docker 的对外端口不同。

```bash
# backend 目录
python -m pytest -q
# frontend 目录
npm run build
```

在项目根目录执行：

```bash
git add .
python scripts/check_publication.py
git diff --cached --stat
```

## 兼容性与来源说明

此项目由已有项目精简而来，不声明全部代码为原创。第三方组件及模型适用各自许可证。初始源码的项目来源标识已保存在 [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md)。本版本不擅自重授许可证；发布者仍应确认上游授权范围，保留必要的来源与版权声明。