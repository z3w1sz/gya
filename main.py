from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Configura el manejo de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# URL base de Areto Accesorios
BASE_URL = "https://aretoaccesorios.com/productos?search="

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('products.html', 'r') as file:
        return file.read()

@app.get("/search", response_class=HTMLResponse)
async def search(query: str = Query(..., min_length=1)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{query}")
        response.raise_for_status()
        html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.select('.single-product')
    
    html_results = ""
    for product in products:
        img_tag = product.select_one('.product-img img')
        link_tag = product.select_one('.product-caption h4 a')
        price_tags = product.select('.price ul li')

        img_src = img_tag['data-src'] if img_tag else ""
        link_href = link_tag['href'] if link_tag else ""
        codigo = link_href.split("/")[-1]
        link_text = link_tag.get_text() if link_tag else ""
        price_text = " ".join([p.get_text() for p in price_tags])
        price = price_text.split("$")[1].split(" ")[0]
        new_price = str(int(int(price) * 1.8))

        # Adaptación para mostrar la imagen a la izquierda y la información a la derecha
        html_results += f"""
        <div class="product-card">
            <img src="{img_src}" alt="{link_text}">
            <div class="product-info">
                <h3><a class="product_link" href="{link_href}">{link_text}</a></h3>
                <p class="original_price">Precio original: <span class="envio_price">${price}</span></p>
                <p class="codigo">Código: {codigo}</p>
                <span class="price">${new_price}</span>
            </div>
        </div>
        """

    # Envolver los resultados en un contenedor grid
    final_html = f"""
    <div class="product-grid">
        {html_results}
    </div>
    """

    return final_html

