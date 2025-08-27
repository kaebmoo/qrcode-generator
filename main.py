from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
from io import BytesIO
from PIL import Image, ImageDraw
from qrcodegen import QrCode
import os
from typing import Optional

app = FastAPI(title="QR Code Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

def generate_qr_code(data: str, with_logo: bool = True):
    """Generate QR Code with optional logo"""
    qr = QrCode.encode_text(data, QrCode.Ecc.QUARTILE)
    size = qr.get_size()
    scale = 8
    img_size = size * scale
    img = Image.new('1', (img_size, img_size), 'white')
    
    # Draw QR Code
    for y in range(size):
        for x in range(size):
            if qr.get_module(x, y):
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((x * scale + dx, y * scale + dy), 0)
    
    # Convert to RGB
    img = img.convert("RGB")
    
    # Add logo if requested and file exists
    if with_logo:
        logo_path = os.path.join('static', '01_NT-Logo.png')
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                
                # Maintain logo ratio
                logo_width, logo_height = logo.size
                logo_ratio = logo_width / logo_height
                max_logo_size = img_size // 5
                
                if logo_width > logo_height:
                    new_logo_width = max_logo_size
                    new_logo_height = int(max_logo_size / logo_ratio)
                else:
                    new_logo_height = max_logo_size
                    new_logo_width = int(max_logo_size * logo_ratio)
                
                logo = logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
                
                # Add white background padding around logo
                padding = 10
                logo_position = ((img_size - new_logo_width) // 2,
                                 (img_size - new_logo_height) // 2)
                
                draw = ImageDraw.Draw(img)
                draw.rectangle([(logo_position[0] - padding, logo_position[1] - padding),
                                (logo_position[0] + new_logo_width + padding,
                                 logo_position[1] + new_logo_height + padding)],
                               fill="white")
                
                # Paste logo
                if logo.mode == 'RGBA':
                    img.paste(logo, logo_position, mask=logo.split()[3])
                else:
                    img.paste(logo, logo_position)
            except Exception as e:
                print(f"Error adding logo: {e}")
    
    return img

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(request: Request, text: str = Form(...), with_logo: Optional[str] = Form(None)):
    """Generate QR Code and return base64 image"""
    if not text:
        raise HTTPException(status_code=400, detail="Text or URL is required")
    
    # Check if checkbox was checked (will be "true" if checked, None if unchecked)
    has_logo = with_logo == "true"
    
    try:
        img = generate_qr_code(text, has_logo)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "qr_image": img_str,
            "text": text[:100] + "..." if len(text) > 100 else text,
            "with_logo": has_logo
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/qrcode")
async def get_qr_image(text: str, with_logo: bool = True):
    """API endpoint to get QR code as image directly"""
    try:
        img = generate_qr_code(text, with_logo)
        
        # Save to BytesIO
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        
        return Response(content=buffered.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{text}")
async def download_qr(text: str, with_logo: bool = True):
    """Download QR Code as PNG file"""
    try:
        img = generate_qr_code(text, with_logo)
        
        # Save to BytesIO
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        
        return StreamingResponse(
            buffered, 
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=qrcode_{text[:20]}.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)