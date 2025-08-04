# qmwneb946 的博客 - 源文件 🚀

> 欢迎来到我的个人博客源文件仓库！这里存放着驱动 [qmwneb946.dpdns.org](https://qmwneb946.dpdns.org) 的所有代码和文章。

这个仓库通过 **Hexo** 生成静态页面，并利用 **GitHub Actions** 实现自动化部署。

[![部署状态](https://github.com/qmwneb946/blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/qmwneb946/blog/actions)
[![最后提交](https://img.shields.io/github/last-commit/qmwneb946/blog)](https://github.com/qmwneb946/blog/commits/main)
[![Node.js 版本](https://img.shields.io/badge/node-20.x-green.svg)](https://nodejs.org/en/)
[![许可证](https://img.shields.io/github/license/qmwneb946/blog)](./LICENSE)

---

## ✨ 线上访问

**点击下方按钮，访问我的博客：**

<p align="center">
  <a href="https://qmwneb946.dpdns.org" target="_blank">
    <img src="https://img.shields.io/badge/访问博客-→-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLW1vdXNlLXBvaW50ZXIiPjxwYXRoIGQ9Im0zIDMgNS41IDEyLjUgNCAuNSAzLjUtNy41TDkgMy41WiIvPjxwYXRoIGQ9Im0xMy41IDEzLjUgNyA3Ii8+PC9zdmc+" alt="访问博客">
  </a>
</p>


## 🛠️ 技术栈

本博客主要由以下技术构建：

| 技术 | 描述 |
| :--- | :--- |
| **Hexo** | 一个快速、简洁且高效的博客框架。 |
| **Node.js** | JavaScript 运行环境，驱动 Hexo。 |
| **Markdown** | 文章编写的标记语言。 |
| **Butterfly** | 一个美观、功能强大的 Hexo 主题。 |
| **GitHub Actions** | 用于自动化构建和部署的 CI/CD 工具。|


## 本地开发指南

如果你想在本地运行或预览这个博客，请遵循以下步骤。

**1. 环境准备**

确保你的电脑上已经安装了 [Node.js](https://nodejs.org/en/) (建议版本 v20.x) 和 [Git](https://git-scm.com/)。

**2. 克隆与安装**

```bash
# 克隆本仓库
git clone [https://github.com/qmwneb946/blog.git](https://github.com/qmwneb946/blog.git)

# 进入项目目录
cd blog

# 安装项目依赖
npm install
```

**3. 本地运行**

执行以下命令来启动本地开发服务器，默认地址为 `http://localhost:4000`。

```bash
# 启动服务器（包含清理缓存）
npx hexo clean && npx hexo s
```

**4. 创建新文章**

使用以下命令可以快速创建一篇新的博文。

```bash
# 新建一篇文章
npx hexo new post "你的文章标题"
```
文件会生成在 `source/_posts` 目录下。

## 🚀 自动化部署

本项目已配置 GitHub Actions 实现自动化部署。

- **触发条件**：任何 `commit` 推送到 `main` 分支。
- **工作流程**：
    1.  Actions 会自动拉取最新代码。
    2.  安装依赖，并执行 `npx hexo g` 生成静态文件。
    3.  将生成的 `public` 目录下的所有内容，自动推送到 `gh-pages` 分支。
- **部署结果**：GitHub Pages 会根据 `gh-pages` 分支的内容来更新线上网站。

你可以在 [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml) 查看详细的部署配置。

## 🙏 致谢

* 感谢 [Hexo](https://hexo.io/) 团队提供了如此出色的博客框架。
* 感谢 [JerryC](https://github.com/jerryc127) 开发了 [Hexo-Theme-Butterfly](https://github.com/jerryc127/hexo-theme-butterfly) 这款精美的主题。

## 📄 许可证

本项目采用 [MIT](./LICENSE) 许可证。