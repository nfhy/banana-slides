# 🍌 蕉幻 (Banana Slides)

一个基于AI的智能PPT生成工具，支持一句话生成完整PPT演示文稿。

## ✨ 项目简介

蕉幻（Banana Slides）是一个AI原生的PPT生成应用，它利用大语言模型（LLM）和文生图模型（nano-banana-pro）来自动化PPT制作流程。用户只需要提供一个简单的想法或大纲，系统就能自动生成包含精美设计的完整PPT。

### 核心亮点

- 🚀 **一句话生成PPT**：从一个简单的想法快速生成完整的演示文稿
- 🎨 **风格模板支持**：支持上传参考图片，生成的PPT将保持统一的设计风格
- ⚡ **并行化处理**：多线程并行生成PPT页面，大幅提升生成速度
- 🔄 **灵活的生成路径**：支持从构想、大纲或详细描述三种方式生成PPT
- 📝 **智能内容生成**：基于LLM自动生成大纲和页面内容描述
- 🖼️ **高质量图片生成**：利用Gemini AI生成4K分辨率、16:9比例的专业设计
- 📊 **完整的PPT导出**：自动组合生成的图片页面并导出为标准PPTX文件

## 🎯 主要功能

### 1. 智能大纲生成
- 根据用户输入的主题自动生成PPT大纲
- 支持简单格式和分章节格式两种组织方式
- 自动识别内容结构，适配最佳展示形式

### 2. 页面描述生成
- 为每一页PPT生成详细的文字描述
- 包含标题、要点、排版建议等完整信息
- 并行化处理，快速生成多页内容

### 3. 图片生成与设计
- 基于页面描述自动生成图片提示词
- 使用Gemini AI的图像生成能力创建精美页面
- 支持参考图片以保持风格一致性
- 并行生成所有页面，提高效率

### 4. PPTX文件生成
- 自动将生成的图片组合成标准PPTX文件
- 16:9比例，适配各种展示场景
- 保持高质量输出

## 🛠️ 技术架构

### 后端技术栈
- **语言**：Python 3.10+
- **包管理**：uv
- **AI能力**：Google Gemini API 
- **PPT处理**：python-pptx
- **并发处理**：ThreadPoolExecutor

### 未来规划
- **前端**：React + TypeScript + Vite
- **状态管理**：Zustand
- **数据持久化**：SQLite
- **后端框架**：Flask

## 📦 安装说明

### 环境要求
- Python 3.10 或更高版本
- 有效的Google Gemini API密钥

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd banana-slides
```

2. **安装依赖**

使用 uv 包管理器：
```bash
uv sync
```

或使用 pip：
```bash
pip install python-pptx google-generativeai pillow
```

3. **配置API密钥**

在 `gemini_genai.py` 中配置你的Gemini API密钥：
```python
genai.configure(api_key="your-api-key-here")
```

## 🚀 快速开始

### 基本使用

```python
from demo import gen_ppt

# 定义你的PPT主题
idea_prompt = "生成一张关于人工智能发展历程的PPT"

# 指定风格参考图（可选）
ref_image = "template_g.png"

# 生成PPT
gen_ppt(idea_prompt, ref_image)
```

### 运行示例

```bash
python demo.py
```

程序会自动：
1. 生成PPT大纲
2. 为每一页生成详细描述
3. 创建图片提示词
4. 并行生成所有页面图片
5. 组合成完整的PPTX文件

### 输出说明

生成的文件会保存在带时间戳的目录中：
- `output_YYYYMMDD_HHMMSS/` - 包含所有生成的单页图片
- `presentation_YYYYMMDD_HHMMSS.pptx` - 最终的PPT文件

## 📁 项目结构

```
banana-slides/
├── demo.py                # 核心PPT生成逻辑
├── gemini_genai.py        # Gemini AI接口封装
├── generate-example.py    # 使用示例
├── PRD.md                 # 产品需求文档
├── 模块设计.md            # 详细模块设计
├── template_g.png         # 样式模板示例
├── pyproject.toml         # 项目配置
└── uv.lock               # 依赖锁定文件
```

## 🔧 核心模块说明

### 1. `gen_outline(idea_prompt)` - 大纲生成
根据用户输入的主题生成PPT大纲结构，支持简单格式和分章节格式。

### 2. `gen_desc(idea_prompt, outline)` - 描述生成
为每一页PPT生成详细的文字描述，包括标题和要点。并行处理提高速度。

### 3. `gen_prompts(outline, desc)` - 提示词生成
根据页面描述生成适合图像生成模型的提示词。

### 4. `gen_images_parallel(prompts, ref_image)` - 图片生成
并行调用AI模型生成所有PPT页面图片。

### 5. `create_pptx_from_images(input_dir)` - PPT组装
将生成的图片组合成标准PPTX文件。

## 💡 使用场景

### 场景1：零基础快速生成
适合对主题有基本想法，但没有具体内容规划的用户：
```python
idea = "介绍量子计算的基本原理和应用"
gen_ppt(idea, "template_g.png")
```

### 场景2：教育演示
快速生成教学用PPT：
```python
idea = "生成一份关于人类活动对生态环境影响的PPT"
gen_ppt(idea, "template_g.png")
```

### 场景3：商业汇报
生成专业的商业演示文稿：
```python
idea = "2024年度市场分析报告"
gen_ppt(idea, "company_template.png")
```

## 🔄 工作流程

```
用户输入主题
    ↓
生成PPT大纲（支持分章节）
    ↓
并行生成每页详细描述
    ↓
生成图片提示词
    ↓
并行生成所有页面图片
    ↓
组装成PPTX文件
    ↓
完成！
```

## ⚙️ 高级配置

### 并发控制
在 `gen_desc()` 中调整描述生成的并发数：
```python
with ThreadPoolExecutor(max_workers=5) as executor:
```

在 `gen_images_parallel()` 中调整图片生成的并发数：
```python
with ThreadPoolExecutor(max_workers=8) as executor:
```

### 图片质量设置
在提示词中可以调整分辨率和比例要求：
```python
要求文字清晰锐利，画面为4k分辨率 16:9比例
```

## 🎨 模板系统

项目支持自定义风格模板：
1. 准备一张符合期望风格的参考图片（建议16:9比例）
2. 在调用 `gen_ppt()` 时传入图片路径
3. 生成的所有PPT页面将保持与参考图风格一致

## 🚧 开发路线图

### 当前版本（v0.1）
- ✅ 命令行版本的核心功能
- ✅ 并行化处理提升性能
- ✅ 支持风格模板参考

### 计划中的功能
- 🔲 Web界面（React + TypeScript）
- 🔲 拖拽式大纲编辑
- 🔲 单页修改与重新生成
- 🔲 多种导出格式（PPTX、PDF）
- 🔲 模板库管理
- 🔲 用户会话保存
- 🔲 更多AI模型支持

## 📝 开发说明

### 代码结构特点
- **并行化设计**：充分利用多线程提升生成速度
- **模块化架构**：每个功能独立封装，易于维护和扩展
- **灵活的大纲结构**：支持扁平和分层两种组织方式
- **完整的错误处理**：生成失败时有明确的提示和重试机制

### 扩展开发
项目采用模块化设计，易于扩展：
- 添加新的AI模型：在 `gemini_genai.py` 中实现新的接口
- 自定义提示词模板：修改 `gen_prompts()` 函数
- 调整PPT样式：修改 `create_pptx_from_images()` 中的参数

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT

## 📞 联系方式

如有问题或建议，欢迎通过Issue反馈。



