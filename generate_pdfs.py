# -*- coding: utf-8 -*-
"""
يولّد ملف PDF واحدًا لكل تلميذ داخل مجلد pdfs/، بنفس رقم التسجيل كاسم للملف.
هذه الملفات هي "قاعدة بيانات" الـ PDF التي يقرأ منها الموقع (script.js) عند
العثور على رقم التسجيل ليحمّل الملف المطابق تلقائيًا.

الاستعمال:
    pip install reportlab arabic-reshaper python-bidi --break-system-packages
    python3 generate_pdfs.py

عدّل مصفوفة RECORDS بالأسفل بنفس شكل البيانات الموجودة في script.js
(يفضّل إبقاء الاثنين متطابقين).
"""

import os
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_REGULAR = "/usr/share/fonts/truetype/kacst/KacstBook.ttf"
FONT_BOLD    = "/usr/share/fonts/truetype/kacst/KacstOffice.ttf"

pdfmetrics.registerFont(TTFont("ArabicRegular", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("ArabicBold", FONT_BOLD))

OUT_DIR = "pdfs"
os.makedirs(OUT_DIR, exist_ok=True)

# نفس بيانات RESULTS_DB الموجودة في script.js
RECORDS = [
    {"reg": "20261001234", "name": "أمين بلحاج",       "track": "علوم تجريبية", "avg": "14.85",
     "school": "متوسطة الأمير عبد القادر", "wilaya": "سطيف", "status": "pass"},
    {"reg": "20261005678", "name": "ياسمين شريط",       "track": "آداب وفلسفة",   "avg": "12.40",
     "school": "متوسطة ابن خلدون",         "wilaya": "سطيف", "status": "pass"},
    {"reg": "20261009012", "name": "عبد الرؤوف مزياني", "track": "تقني رياضي",    "avg": "15.20",
     "school": "متوسطة الشهيد بوعزيز",     "wilaya": "سطيف", "status": "pass"},
    {"reg": "20261003456", "name": "إيمان بوداود",      "track": "لغات أجنبية",   "avg": "13.65",
     "school": "متوسطة العقيد لطفي",       "wilaya": "سطيف", "status": "pass"},
    {"reg": "20261007890", "name": "محمد أمين طواهرية", "track": "—",             "avg": "08.10",
     "school": "متوسطة الإخوة بوعدو",      "wilaya": "سطيف", "status": "fail"},
]


def ar(text):
    """يهيئ النص العربي للعرض الصحيح داخل PDF (تشكيل الحروف + اتجاه الكتابة)."""
    return get_display(arabic_reshaper.reshape(text))


def draw_label_value(c, page_w, margin, y, label, value, bold_value=False):
    c.setFont("ArabicBold", 12)
    c.drawRightString(page_w - margin, y, ar(label))
    c.setFont("ArabicBold" if bold_value else "ArabicRegular", 12)
    c.drawRightString(page_w - margin - 190, y, ar(value))


def make_pdf(rec, path):
    page_w, page_h = A4
    c = canvas.Canvas(path, pagesize=A4)
    margin = 50

    # الشريط العلوي
    c.setFillColorRGB(0x12/255, 0x23/255, 0x3d/255)
    c.rect(0, page_h - 90, page_w, 90, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("ArabicBold", 16)
    c.drawCentredString(page_w/2, page_h - 42, ar("شهادة استظهار نتيجة اختبار تحديد الشعبة"))
    c.setFont("ArabicRegular", 11)
    c.drawCentredString(page_w/2, page_h - 62, ar("دورة جوان 2026"))

    y = page_h - 140
    c.setFillColorRGB(0x12/255, 0x23/255, 0x3d/255)

    draw_label_value(c, page_w, margin, y, "رقم التسجيل :", rec["reg"]); y -= 28
    draw_label_value(c, page_w, margin, y, "الاسم واللقب :", rec["name"], bold_value=True); y -= 28
    draw_label_value(c, page_w, margin, y, "المؤسسة الأصلية :", rec["school"]); y -= 28
    draw_label_value(c, page_w, margin, y, "الولاية :", rec["wilaya"]); y -= 28
    draw_label_value(c, page_w, margin, y, "المعدل العام :", rec["avg"] + " / 20"); y -= 28
    status_txt = "ناجح" if rec["status"] == "pass" else "غير ناجح"
    draw_label_value(c, page_w, margin, y, "النتيجة :", status_txt, bold_value=True)

    # مربع الشعبة
    y -= 46
    box_h = 60
    c.setFillColorRGB(0xf1/255, 0xe2/255, 0xbc/255)
    c.setStrokeColorRGB(0xb8/255, 0x86/255, 0x2c/255)
    c.roundRect(margin, y - box_h, page_w - margin*2, box_h, 8, fill=1, stroke=1)
    c.setFillColorRGB(0x5c/255, 0x41/255, 0x10/255)
    c.setFont("ArabicBold", 11)
    c.drawCentredString(page_w/2, y - 22, ar("الشعبة المحصل عليها"))
    c.setFont("ArabicBold", 18)
    c.drawCentredString(page_w/2, y - 46, ar(rec["track"]))

    # تذييل
    c.setFillColorRGB(0x5a/255, 0x65/255, 0x77/255)
    c.setFont("ArabicRegular", 9)
    c.drawCentredString(page_w/2, 60, ar("هذه الوثيقة مخصصة للاستظهار المحلي ولا تُغني عن الوثيقة الرسمية الصادرة عن المؤسسة."))

    c.showPage()
    c.save()


if __name__ == "__main__":
    for rec in RECORDS:
        out_path = os.path.join(OUT_DIR, f"{rec['reg']}.pdf")
        make_pdf(rec, out_path)
        print("تم إنشاء:", out_path)
