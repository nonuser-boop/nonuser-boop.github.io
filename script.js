// ------------------------------------------------------------------
// قاعدة البيانات: استبدل هذه المصفوفة ببيانات النتائج الحقيقية.
// كل سجل يمثل تلميذًا واحدًا. رقم التسجيل (reg) هو مفتاح البحث.
// حقل "pdf" هو مسار ملف النتيجة الجاهز (PDF) الخاص بهذا التلميذ،
// الموجود داخل مجلد pdfs/. عند العثور على الرقم يتم تحميل هذا
// الملف تلقائيًا من غير الحاجة لأي زر.
//
// لتوليد ملفات PDF جديدة لتلاميذ حقيقيين، استعمل السكريبت المرفق
// generate_pdfs.py (يقرأ نفس شكل البيانات وينتج ملفًا لكل سجل).
// ------------------------------------------------------------------
const RESULTS_DB = [
  { reg:"0001", name:"لؤي جابوربي ",        track:"راسب", avg:"0.13", school:"", wilaya:"", status:"fail", pdf:"0001.pdf" },
  { reg:"0002", name:"بن دحمان شيماء ",        track:"شعبة الرياضيات",   avg:"16.89", school:"",         wilaya:"", status:"pass", pdf:"0002.pdf" },
  { reg:"0003", name:"بن دحمان نوح ",  track:"اللغة العربية و ادابها",    avg:"3.86", school:ز",     wilaya:"", status:"pass", pdf:"0003.pdf" },
  { reg:"20261003456", name:"إيمان بوداود",       track:"لغات أجنبية",   avg:"13.65", school:"متوسطة العقيد لطفي",       wilaya:"سطيف", status:"pass", pdf:"pdfs/20261003456.pdf" },
  { reg:"20261007890", name:"محمد أمين طواهرية",  track:"—",             avg:"08.10", school:"متوسطة الإخوة بوعدو",      wilaya:"سطيف", status:"fail", pdf:"pdfs/20261007890.pdf" },
];

const form = document.getElementById('lookupForm');
const input = document.getElementById('regInput');
const errorMsg = document.getElementById('errorMsg');
const infoMsg = document.getElementById('infoMsg');
const ticket = document.getElementById('ticket');
let currentRecord = null;

const arabicIndicToWestern = (s) => s.replace(/[\u0660-\u0669]/g, d => String(d.charCodeAt(0) - 0x0660));

function normalize(v){
  return arabicIndicToWestern(v).trim().replace(/\s+/g,'');
}

function findRecord(reg){
  const clean = normalize(reg);
  return RESULTS_DB.find(r => normalize(r.reg) === clean);
}

function todayArabic(){
  const d = new Date();
  return d.toLocaleDateString('ar-DZ', { year:'numeric', month:'long', day:'numeric' });
}

function renderRecord(rec){
  document.getElementById('outName').textContent = rec.name;
  document.getElementById('outReg').textContent = 'رقم التسجيل: ' + rec.reg;
  document.getElementById('outTrack').textContent = rec.track;
  document.getElementById('outAvg').textContent = rec.avg + ' / 20';
  document.getElementById('outSchool').textContent = rec.school;
  document.getElementById('outWilaya').textContent = rec.wilaya;
  document.getElementById('outDate').textContent = todayArabic();

  const statusEl = document.getElementById('outStatus');
  if(rec.status === 'pass'){
    statusEl.textContent = 'ناجح';
    statusEl.className = 'status-badge pass';
  } else {
    statusEl.textContent = 'غير ناجح';
    statusEl.className = 'status-badge fail';
  }

  ticket.style.display = 'block';
  errorMsg.style.display = 'none';
}

// يطلق تحميل ملف الـ PDF الخاص بالسجل مباشرة من مجلد قاعدة البيانات pdfs/
function triggerDownload(rec){
  const a = document.createElement('a');
  a.href = rec.pdf;
  a.download = 'نتيجة-' + rec.reg + '.pdf';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const rec = findRecord(input.value);
  infoMsg.style.display = 'none';

  if(rec){
    currentRecord = rec;
    renderRecord(rec);
    ticket.scrollIntoView({behavior:'smooth', block:'nearest'});

    // تحميل تلقائي فور العثور على النتيجة
    triggerDownload(rec);
    infoMsg.textContent = 'تم العثور على النتيجة، وبدأ تحميل ملف PDF تلقائيًا.';
    infoMsg.style.display = 'block';
  } else {
    currentRecord = null;
    ticket.style.display = 'none';
    errorMsg.style.display = 'block';
  }
});

document.getElementById('resetBtn').addEventListener('click', () => {
  input.value = '';
  ticket.style.display = 'none';
  errorMsg.style.display = 'none';
  infoMsg.style.display = 'none';
  currentRecord = null;
  input.focus();
});

// زر لإعادة تحميل نفس الملف يدويًا عند الحاجة
document.getElementById('downloadBtn').addEventListener('click', () => {
  if(!currentRecord) return;
  triggerDownload(currentRecord);
});
