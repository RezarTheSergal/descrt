import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from settings import CLOUDINARY_CLIENT_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from datetime import datetime

class CloudinaryImaging:

    def __init__(self):
        cloudinary.config(
            cloud_name=CLOUDINARY_CLIENT_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )

    def upload_img(self, image_name, img_type, path):
        try:
            response = cloudinary.uploader.upload(
                path, 
                public_id=f"{image_name}_{img_type}_{datetime.now().strftime('%d_%m_%Y_%H:%M:%S.%f')}", 
                tags=[image_name, img_type]
            )
            return response
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            return None

    def get_img_urls(self, image_name, **kwargs) -> list[str]:
        """
        Возвращает список URL всех изображений с заданным тегом
        
        Args:
            image_name: тег для поиска изображений
            **kwargs: параметры для преобразования Cloudinary
        
        Returns:
            list[str]: список URL или пустой список при ошибке
        """
        try:
            result = cloudinary.api.resources_by_tag(tag=image_name)
            
            if not result.get('resources'):
                print(f"Изображения с тегом '{image_name}' не найдены")
                return []
            
            urls = []
            for resource in result['resources']:
                public_id = resource['public_id']
                url, _ = cloudinary.utils.cloudinary_url(
                    public_id, 
                    fetch_format="auto", 
                    quality="auto", 
                    **kwargs
                )
                urls.append(url)
            
            return urls
            
        except Exception as e:
            print(f"Ошибка при получении изображений: {e}")
            return []
