from crawl4ai import AsyncWebCrawler

class CrawlService:
    async def fetch_government_data(self, url: str) -> str:
        """
        Realiza o crawling de portais governamentais de forma assíncrona.
        O Crawl4AI é otimizado para extrair conteúdo limpo para LLMs.
        """
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=url,
                bypass_cache=True
            )
            
            if result.success:
                # Retorna o markdown simplificado, ideal para processamento de IA
                return result.markdown
            
            return f"Erro ao acessar {url}: {result.error_message}"