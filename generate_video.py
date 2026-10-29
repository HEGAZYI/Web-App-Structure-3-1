#!/usr/bin/env python3
"""
Generate educational video frames showing 3-layer web app architecture interaction.
Arabic RTL labels, professional colors, packet animation.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    try:
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

OUT_DIR = "/home/workdir/artifacts/webapp-architecture/video_frames"
W, H = 960, 540
FPS = 15
DURATION = 12  # seconds
TOTAL = FPS * DURATION

# Colors
BG = (15, 23, 42)
FRONTEND = (13, 110, 253)
BACKEND = (25, 135, 84)
DATABASE = (253, 126, 20)
WHITE = (255, 255, 255)
LIGHT = (226, 232, 240)
MUTED = (148, 163, 184)
PACKET = (244, 114, 182)
ACCENT = (96, 165, 250)

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/SlidesCarnival/google/Noto Sans Arabic/static/NotoSansArabic-Bold.ttf" if bold else "/usr/share/fonts/SlidesCarnival/google/Noto Sans Arabic/static/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/SlidesCarnival/google/Cairo/Cairo-VariableFont_slnt,wght.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_layer_box(draw, x, y, w, h, color, title, subtitle, icon_char, font_t, font_s, active=False):
    bg = (*color, 40) if not active else (*color, 80)
    # Outer glow when active
    if active:
        for i in range(6, 0, -1):
            alpha = 20 + i * 8
            rounded_rect(draw, (x - i, y - i, x + w + i, y + h + i), 18, None, outline=(*color, alpha), width=2)
    rounded_rect(draw, (x, y, x + w, y + h), 16, fill=(30, 41, 59), outline=color, width=3 if active else 2)
    # top bar
    draw.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 36], radius=12, fill=color)
    draw.text((x + w // 2, y + 18), title, font=font_t, fill=WHITE, anchor="mm")
    draw.text((x + w // 2, y + h // 2 + 10), subtitle, font=font_s, fill=LIGHT, anchor="mm")
    # simple icon circle
    cx, cy = x + w // 2, y + 58
    draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=color)
    draw.text((cx, cy), icon_char, font=font_t, fill=WHITE, anchor="mm")

def lerp(a, b, t):
    return a + (b - a) * t

def ease_in_out(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, t)))

def draw_packet(draw, x, y, label, font, going_down=True):
    r = 14
    color = PACKET if going_down else (74, 222, 128)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    # small trail
    for i in range(1, 4):
        tr = r - i * 3
        if tr > 2:
            ty = y - i * 12 if going_down else y + i * 12
            alpha_fill = (color[0], color[1], color[2])
            draw.ellipse([x - tr, ty - tr, x + tr, ty + tr], outline=alpha_fill, width=1)
    if label:
        draw.text((x, y - 28 if going_down else y + 28), label, font=font, fill=WHITE, anchor="mm")

def draw_arrow_line(draw, x1, y1, x2, y2, color, width=3):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    ah = 12
    ax1 = x2 - ah * math.cos(angle - 0.4)
    ay1 = y2 - ah * math.sin(angle - 0.4)
    ax2 = x2 - ah * math.cos(angle + 0.4)
    ay2 = y2 - ah * math.sin(angle + 0.4)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def make_frame(frame_idx):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")

    font_title = get_font(28, bold=True)
    font_layer = get_font(18, bold=True)
    font_sub = get_font(14)
    font_step = get_font(16, bold=True)
    font_small = get_font(13)
    font_big = get_font(36, bold=True)

    t = frame_idx / TOTAL  # 0..1

    # Title
    draw.text((W // 2, 40), ar("تفاعل الطبقات الثلاث في تطبيق الويب"), font=font_title, fill=WHITE, anchor="mm")
    draw.text((W // 2, 72), "Frontend  →  Backend  →  Database", font=font_small, fill=MUTED, anchor="mm")

    # Layer positions (centered vertically chain)
    box_w, box_h = 280, 140
    cx = W // 2
    gap = 55
    y_fe = 120
    y_be = y_fe + box_h + gap
    y_db = y_be + box_h + gap

    # Timeline phases (0-1)
    # 0.00-0.08  intro
    # 0.08-0.22  user types / FE active
    # 0.22-0.36  packet FE → BE
    # 0.36-0.50  packet BE → DB
    # 0.50-0.64  packet DB → BE
    # 0.64-0.78  packet BE → FE
    # 0.78-0.92  FE shows result
    # 0.92-1.00  hold / summary

    phase = t
    active_fe = False
    active_be = False
    active_db = False
    packet_pos = None  # (x, y, going_down, label)
    step_text = ""
    step_color = ACCENT

    if phase < 0.08:
        step_text = ar("ابدأ: المستخدم يريد البحث عن منتج...")
    elif phase < 0.22:
        active_fe = True
        step_text = ar("١. الواجهة الأمامية تستقبل كلمات البحث من المستخدم")
        step_color = FRONTEND
    elif phase < 0.36:
        active_fe = True
        active_be = True
        p = ease_in_out((phase - 0.22) / 0.14)
        y = lerp(y_fe + box_h, y_be, p)
        packet_pos = (cx, y, True, ar("طلب"))
        step_text = ar("٢. إرسال الطلب من الواجهة الأمامية → الواجهة الخلفية")
        step_color = FRONTEND
    elif phase < 0.50:
        active_be = True
        active_db = True
        p = ease_in_out((phase - 0.36) / 0.14)
        y = lerp(y_be + box_h, y_db, p)
        packet_pos = (cx, y, True, ar("استعلام"))
        step_text = ar("٣. الواجهة الخلفية تطلب البيانات من قاعدة البيانات")
        step_color = BACKEND
    elif phase < 0.64:
        active_be = True
        active_db = True
        p = ease_in_out((phase - 0.50) / 0.14)
        y = lerp(y_db, y_be + box_h, p)
        packet_pos = (cx, y, False, ar("نتائج"))
        step_text = ar("٤. قاعدة البيانات تُرجع النتائج إلى الواجهة الخلفية")
        step_color = DATABASE
    elif phase < 0.78:
        active_fe = True
        active_be = True
        p = ease_in_out((phase - 0.64) / 0.14)
        y = lerp(y_be, y_fe + box_h, p)
        packet_pos = (cx, y, False, ar("استجابة"))
        step_text = ar("٥. الواجهة الخلفية تجهّز النتيجة وترسلها للواجهة الأمامية")
        step_color = BACKEND
    elif phase < 0.92:
        active_fe = True
        step_text = ar("٦. الواجهة الأمامية تعرض نتائج البحث للمستخدم ✓")
        step_color = FRONTEND
    else:
        active_fe = active_be = active_db = True
        step_text = ar("ثلاث طبقات متعاونة: عرض • معالجة • تخزين")
        step_color = ACCENT

    # Connection lines (static rails)
    line_color = (51, 65, 85)
    draw.line([(cx, y_fe + box_h), (cx, y_be)], fill=line_color, width=4)
    draw.line([(cx, y_be + box_h), (cx, y_db)], fill=line_color, width=4)

    # Highlight path during travel
    if 0.22 <= phase < 0.36:
        draw.line([(cx, y_fe + box_h), (cx, packet_pos[1])], fill=FRONTEND, width=4)
    elif 0.36 <= phase < 0.50:
        draw.line([(cx, y_be + box_h), (cx, packet_pos[1])], fill=BACKEND, width=4)
    elif 0.50 <= phase < 0.64:
        draw.line([(cx, packet_pos[1]), (cx, y_be + box_h)], fill=DATABASE, width=4)
    elif 0.64 <= phase < 0.78:
        draw.line([(cx, packet_pos[1]), (cx, y_fe + box_h)], fill=BACKEND, width=4)

    # Draw boxes
    draw_layer_box(draw, cx - box_w // 2, y_fe, box_w, box_h, FRONTEND,
                   ar("الواجهة الأمامية"), "Frontend  •  " + ar("عرض وتفاعل"), "F", font_layer, font_sub, active_fe)
    draw_layer_box(draw, cx - box_w // 2, y_be, box_w, box_h, BACKEND,
                   ar("الواجهة الخلفية"), "Backend  •  " + ar("معالجة وقواعد"), "B", font_layer, font_sub, active_be)
    draw_layer_box(draw, cx - box_w // 2, y_db, box_w, box_h, DATABASE,
                   ar("قاعدة البيانات"), "Database  •  " + ar("تخزين واسترجاع"), "D", font_layer, font_sub, active_db)

    # Packet
    if packet_pos:
        draw_packet(draw, packet_pos[0], packet_pos[1], packet_pos[3], font_small, packet_pos[2])

    # User icon on the left of Frontend during first phases
    if phase < 0.36 or (0.78 <= phase < 0.92):
        ux = cx - box_w // 2 - 90
        uy = y_fe + box_h // 2
        draw.ellipse([ux - 28, uy - 28, ux + 28, uy + 28], fill=(51, 65, 85), outline=PACKET, width=2)
        draw.text((ux, uy - 5), "👤", font=font_big, anchor="mm")
        draw.text((ux, uy + 38), ar("المستخدم"), font=font_small, fill=MUTED, anchor="mm")
        if phase < 0.22:
            # typing dots
            dots = int((phase * 40) % 4)
            draw.text((ux + 50, uy), ar("بحث") + "." * dots, font=font_small, fill=LIGHT, anchor="mm")

    # Step banner at bottom
    banner_h = 56
    draw.rounded_rectangle([40, H - banner_h - 24, W - 40, H - 24], radius=14, fill=(30, 41, 59), outline=step_color, width=2)
    draw.text((W // 2, H - banner_h // 2 - 24), step_text, font=font_step, fill=WHITE, anchor="mm")

    # Progress bar
    bar_y = H - 12
    draw.rectangle([0, bar_y, W, H], fill=(30, 41, 59))
    draw.rectangle([0, bar_y, int(W * t), H], fill=step_color)

    # Side labels
    draw.text((40, y_fe + box_h // 2), ar("عرض") + "\n" + ar("وتجميع"), font=font_small, fill=FRONTEND, anchor="lm")
    draw.text((40, y_be + box_h // 2), ar("معالجة") + "\n" + ar("وتحكم"), font=font_small, fill=BACKEND, anchor="lm")
    draw.text((40, y_db + box_h // 2), ar("تخزين") + "\n" + ar("واسترجاع"), font=font_small, fill=DATABASE, anchor="lm")

    return img.convert("RGB")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Generating {TOTAL} frames at {FPS} fps ({DURATION}s)...")
    for i in range(TOTAL):
        frame = make_frame(i)
        frame.save(os.path.join(OUT_DIR, f"frame_{i:04d}.png"))
        if i % 30 == 0:
            print(f"  frame {i}/{TOTAL}")
    print("Done frames.")

if __name__ == "__main__":
    main()
