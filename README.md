# 🛍️ Shopify Tools

通过 Shopify Admin GraphQL API + GitHub Actions 自动对商品集合（Collection）进行排序。  
支持基于「30 天销量」和「上新时间」进行排序，自动维护 Best Selling 商品集合。

---

## 🚀 功能概览

- ✅ 自动排序 Shopify 集合：销量优先 + 新品插位
- ✅ 支持 GitHub Actions 定时任务（每天自动更新）
- ✅ 支持本地调试（使用 `.env` 配置）
- ✅ 采用 Shopify GraphQL API（更高效更灵活）
- ✅ 多集合可扩展（可增加新品榜、清仓榜等）
- ✅ 开箱即用，可部署在公共或私有 GitHub 仓库

---

## 📦 排序逻辑说明（Best Selling）

### Best Selling

1. **30 天内有销量商品**，按销量倒序排列  
2. **30 天内上架的新品**：插入第 5～8 位（保留最多 4 个）  
   - 若新品不足 4 个：用销量商品补位  
   - 若新品超过 4 个：仅取最新 4 个  
3. **30 天内无销量商品**：放到最后，按上新时间倒序排列  

---

## 🛠️ 本地运行指南

### 1. 克隆项目

```bash
git clone https://github.com/zhangkkan/shopify-tools
cd shopify-tools
pip install -r requirements.txt
```

### 2. 创建 .env 文件

复制 .env.example 为 .env 并填写真实值：

```bash
cp .env.example .env
```

.env 示例：

```env
SHOP_NAME=your-store.myshopify.com
ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxx
COLLECTION_GID=gid://shopify/Collection/1234567890
```

### 3. 运行脚本

```bash
python -m scripts.best_selling
```

---

## 🧩 项目结构说明

```bash
shopify-collection-sorter/
├── .github/workflows/
│   └── sync_collections.yml   # GitHub Actions 工作流
├── scripts/
│   └── best_selling.py        # Best Selling 脚本
├── utils/
│   └── shopify_client.py      # GraphQL API 封装
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量模板
└── README.md
```

---

## 🔁 自动化部署（GitHub Actions）

项目已内置 GitHub Actions 工作流，可定时自动运行。

### 1. 推送到你的 GitHub 仓库

```bash
git init
git remote add origin https://github.com/yourname/shopify-collection-sorter.git
git add .
git commit -m "init"
git push -u origin main
```

### 2. 配置 Secrets

前往仓库 → Settings → Secrets and variables → Actions → 添加以下变量：

| 名称                            | 示例值                            |
| ----------------------------- | ------------------------------ |
| `SHOP_NAME`                   | `your-store.myshopify.com`     |
| `ACCESS_TOKEN`                | `shpat_...`（Private App Token） |
| `COLLECTION_GID_BEST_SELLING` | `gid://shopify/Collection/...` |

### 3. 启用 Actions

推送后，GitHub Actions 会每天自动运行（默认 UTC 00:00，即北京时间早上 8 点）
也可手动点击 “Run workflow” 触发。

---

## 📄 License

MIT License
本项目可自由商用、修改、部署，欢迎 Fork 或 Star ⭐！

---

## 🙌 作者

由 zhangkkan 编写，如有问题欢迎提 Issue。

---