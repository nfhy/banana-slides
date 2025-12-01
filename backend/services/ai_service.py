"""
AI Service - handles all AI model interactions
Based on demo.py and gemini_genai.py
"""
import os
import json
from typing import List, Dict, Optional
from textwrap import dedent
from google import genai
from google.genai import types
from PIL import Image
import os


class AIService:
    """Service for AI model interactions using Gemini"""
    
    def __init__(self, api_key: str, api_base: str = None):
        """Initialize AI service with API credentials"""
        # Always create HttpOptions, matching gemini_genai.py behavior
        self.client = genai.Client(
            http_options=types.HttpOptions(
                base_url=api_base
            ),
            api_key=api_key
        )
        self.text_model = "gemini-2.5-flash"
        self.image_model = "gemini-3-pro-image-preview"
    
    def generate_outline(self, idea_prompt: str) -> List[Dict]:
        """
        Generate PPT outline from idea prompt
        Based on demo.py gen_outline()
        
        Returns:
            List of outline items (may contain parts with pages or direct pages)
        """
        outline_prompt = dedent(f"""\
        You are a helpful assistant that generates an outline for a ppt.
        
        You can organize the content in two ways:
        
        1. Simple format (for short PPTs without major sections):
        [{{"title": "title1", "points": ["point1", "point2"]}}, {{"title": "title2", "points": ["point1", "point2"]}}]
        
        2. Part-based format (for longer PPTs with major sections):
        [
          {{
            "part": "Part 1: Introduction",
            "pages": [
              {{"title": "Welcome", "points": ["point1", "point2"]}},
              {{"title": "Overview", "points": ["point1", "point2"]}}
            ]
          }},
          {{
            "part": "Part 2: Main Content",
            "pages": [
              {{"title": "Topic 1", "points": ["point1", "point2"]}},
              {{"title": "Topic 2", "points": ["point1", "point2"]}}
            ]
          }}
        ]
        
        Choose the format that best fits the content. Use parts when the PPT has clear major sections.
        
        The user's request: {idea_prompt}. Now generate the outline, don't include any other text.
        使用全中文输出。
        """)
        
        response = self.client.models.generate_content(
            model=self.text_model,
            contents=outline_prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1000),
            ),
        )
        
        outline_text = response.text.strip().strip("```json").strip("```").strip()
        outline = json.loads(outline_text)
        return outline
    
    def flatten_outline(self, outline: List[Dict]) -> List[Dict]:
        """
        Flatten outline structure to page list
        Based on demo.py flatten_outline()
        """
        pages = []
        for item in outline:
            if "part" in item and "pages" in item:
                # This is a part, expand its pages
                for page in item["pages"]:
                    page_with_part = page.copy()
                    page_with_part["part"] = item["part"]
                    pages.append(page_with_part)
            else:
                # This is a direct page
                pages.append(item)
        return pages
    
    def generate_page_description(self, idea_prompt: str, outline: List[Dict], 
                                 page_outline: Dict, page_index: int) -> str:
        """
        Generate description for a single page
        Based on demo.py gen_desc() logic
        
        Args:
            idea_prompt: Original user idea
            outline: Complete outline
            page_outline: Outline for this specific page
            page_index: Page number (1-indexed)
        
        Returns:
            Text description for the page
        """
        part_info = f"\nThis page belongs to: {page_outline['part']}" if 'part' in page_outline else ""
        
        desc_prompt = dedent(f"""\
        we are generating the text desciption for each ppt page.
        the original user request is: \n{idea_prompt}\n
        We already have the entire ouline: \n{outline}\n{part_info}
        Now please generate the description for page {page_index}:
        {page_outline}
        The description includes page title, text to render(keep it concise).
        For example:
        页面标题：原始社会：与自然共生
        页面文字：
        - 狩猎采集文明： 人类活动规模小，对环境影响有限。
        - 依赖性强： 生活完全依赖于自然资源的直接供给，对自然规律敬畏。
        - 适应而非改造： 通过观察和模仿学习自然，发展出适应当地环境的生存技能。
        - 影响特点： 局部、短期、低强度，生态系统有充足的自我恢复能力。
        
        使用全中文输出。
        """)
        
        response = self.client.models.generate_content(
            model=self.text_model,
            contents=desc_prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1000),
            ),
        )
        
        page_desc = response.text
        return dedent(page_desc)
    
    def generate_outline_text(self, outline: List[Dict]) -> str:
        """
        Convert outline to text format for prompts
        Based on demo.py gen_outline_text()
        """
        text_parts = []
        for i, item in enumerate(outline, 1):
            if "part" in item and "pages" in item:
                text_parts.append(f"{i}. {item['part']}")
            else:
                text_parts.append(f"{i}. {item.get('title', 'Untitled')}")
        result = "\n".join(text_parts)
        return dedent(result)
    
    def generate_image_prompt(self, outline: List[Dict], page: Dict, 
                            page_desc: str, page_index: int) -> str:
        """
        Generate image generation prompt for a page
        Based on demo.py gen_prompts()
        
        Args:
            outline: Complete outline
            page: Page outline data
            page_desc: Page description text
            page_index: Page number (1-indexed)
        
        Returns:
            Image generation prompt
        """
        outline_text = self.generate_outline_text(outline)
        
        # Determine current section
        if 'part' in page:
            current_section = page['part']
        else:
            current_section = f"{page.get('title', 'Untitled')}"
        
        prompt = dedent(f"""\
        利用专业平面设计知识，根据参考图片的色彩与风格生成一页设计风格相同的ppt页面，作为整个ppt的其中一页，内容是:
        {page_desc}
        
        整个ppt的大纲为：
        {outline_text}
        
        当前位于章节：{current_section}
        
        要求文字清晰锐利，画面为4k分辨率 16:9比例.画面风格与配色保持严格一致。ppt使用全中文。
        """)
        
        return prompt
    
    def generate_image(self, prompt: str, ref_image_path: str, 
                      aspect_ratio: str = "16:9", resolution: str = "2K") -> Optional[Image.Image]:
        """
        Generate image using Gemini image model
        Based on gemini_genai.py gen_image()
        
        Args:
            prompt: Image generation prompt
            ref_image_path: Path to reference image
            aspect_ratio: Image aspect ratio (currently not used, kept for compatibility)
            resolution: Image resolution (currently not used, kept for compatibility)
        
        Returns:
            PIL Image object or None if failed
        
        Raises:
            Exception with detailed error message if generation fails
        """
        try:
            print(f"[DEBUG] Generating image with prompt (first 100 chars): {prompt[:100]}...")
            print(f"[DEBUG] Reference image: {ref_image_path}")
            print(f"[DEBUG] Config - aspect_ratio: {aspect_ratio}, resolution: {resolution}")
            
            # Check if reference image exists
            if not os.path.exists(ref_image_path):
                raise FileNotFoundError(f"Reference image not found: {ref_image_path}")
            
            print(f"[DEBUG] Calling Gemini API for image generation...")
            response = self.client.models.generate_content(
                model=self.image_model,
                contents=[
                    prompt,
                    Image.open(ref_image_path),
                ],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=resolution
                    ),
                )
            )
            print(f"[DEBUG] Gemini API call completed")
            
            print(f"[DEBUG] API response received, checking parts...")
            for i, part in enumerate(response.parts):
                if part.text is not None:   
                    print(f"[DEBUG] Part {i}: TEXT - {part.text[:100]}")
                else:
                    # Try to get image from part
                    try:
                        print(f"[DEBUG] Part {i}: Attempting to extract image...")
                        image = part.as_image()
                        if image:
                            # Don't check image.size - it might not be a standard PIL Image yet
                            print(f"[DEBUG] Successfully extracted image from part {i}")
                            return image
                    except Exception as e:
                        print(f"[DEBUG] Part {i}: Failed to extract image - {str(e)}")
            
            # If we get here, no image was found in the response
            error_msg = "No image found in API response. "
            if response.parts:
                error_msg += f"Response had {len(response.parts)} parts but none contained valid images."
            else:
                error_msg += "Response had no parts."
            
            raise ValueError(error_msg)
            
        except Exception as e:
            error_detail = f"Error generating image: {type(e).__name__}: {str(e)}"
            print(f"[ERROR] {error_detail}")
            import traceback
            traceback.print_exc()
            raise Exception(error_detail) from e
    
    def edit_image(self, prompt: str, current_image_path: str,
                  aspect_ratio: str = "16:9", resolution: str = "2K") -> Optional[Image.Image]:
        """
        Edit existing image with natural language instruction
        Uses current image as reference
        
        Args:
            prompt: Edit instruction
            current_image_path: Path to current page image
            aspect_ratio: Image aspect ratio
            resolution: Image resolution
        
        Returns:
            PIL Image object or None if failed
        """
        edit_instruction = f"根据以下指令修改这张PPT页面：{prompt}\n保持原有的内容结构和设计风格，只按照指令进行修改。"
        return self.generate_image(edit_instruction, current_image_path, aspect_ratio, resolution)

