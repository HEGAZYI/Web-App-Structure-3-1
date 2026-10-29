$(document).ready(function () {
  // Navbar scroll effect
  $(window).on('scroll', function () {
    if ($(this).scrollTop() > 50) {
      $('.glass-nav').addClass('scrolled');
    } else {
      $('.glass-nav').removeClass('scrolled');
    }
  });

  // Smooth scroll for nav links
  $('a[href^="#"]').on('click', function (e) {
    e.preventDefault();
    const target = $(this.getAttribute('href'));
    if (target.length) {
      $('html, body').animate({ scrollTop: target.offset().top - 70 }, 600);
      $('.navbar-collapse').collapse('hide');
    }
  });

  // ========== Interactive Flow Animation ==========
  let flowRunning = false;
  const steps = $('.flow-step');
  const arrows = $('.flow-arrow');

  const logMessages = [
    { cls: 'log-user', text: '👤 المستخدم يكتب: "سماعات بلوتوث"' },
    { cls: 'log-frontend', text: '🖥️  [Frontend] استقبلت كلمات البحث → إرسال طلب API' },
    { cls: 'log-backend', text: '⚙️  [Backend] استقبلت الطلب → جاري تطبيق قواعد البحث' },
    { cls: 'log-db', text: '🗄️  [Database] استعلام: SELECT * FROM products WHERE name LIKE ...' },
    { cls: 'log-db', text: '🗄️  [Database] أعادت 12 منتجًا مطابقًا' },
    { cls: 'log-backend', text: '⚙️  [Backend] تجهيز JSON + تطبيق الترتيب حسب التقييم' },
    { cls: 'log-frontend', text: '🖥️  [Frontend] عرض 12 نتيجة على الشاشة ✅' }
  ];

  function resetFlowUI() {
    steps.removeClass('active done');
    arrows.removeClass('active');
    $('#liveLog').empty();
    flowRunning = false;
    $('#playFlow').prop('disabled', false).html('<i class="fas fa-play me-2"></i> تشغيل التدفق التفاعلي');
    $('#resetFlow').prop('disabled', true);
  }

  function addLog(msg) {
    const $line = $('<div class="log-line ' + msg.cls + '"></div>').text(msg.text);
    $('#liveLog').append($line);
    $('#liveLog').scrollTop($('#liveLog')[0].scrollHeight);
  }

  $('#playFlow').on('click', function () {
    if (flowRunning) return;
    flowRunning = true;
    $(this).prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i> جاري التشغيل...');
    $('#resetFlow').prop('disabled', false);
    $('#liveLog').empty();

    let i = 0;
    const total = steps.length;

    function nextStep() {
      if (i > 0) {
        steps.eq(i - 1).removeClass('active').addClass('done');
        if (i - 1 < arrows.length) arrows.eq(i - 1).addClass('active');
      }

      if (i < total) {
        steps.eq(i).addClass('active');
        // Log messages aligned with steps
        if (i === 0) {
          addLog(logMessages[0]);
          setTimeout(() => addLog(logMessages[1]), 400);
        } else if (i === 1) {
          addLog(logMessages[2]);
        } else if (i === 2) {
          addLog(logMessages[3]);
        } else if (i === 3) {
          addLog(logMessages[4]);
        } else if (i === 4) {
          addLog(logMessages[5]);
        } else if (i === 5) {
          addLog(logMessages[6]);
        }

        i++;
        setTimeout(nextStep, 1600);
      } else {
        steps.eq(total - 1).removeClass('active').addClass('done');
        flowRunning = false;
        $('#playFlow').prop('disabled', false).html('<i class="fas fa-check me-2"></i> اكتمل التدفق');
      }
    }

    nextStep();
  });

  $('#resetFlow').on('click', resetFlowUI);

  // ========== Quiz ==========
  const quizData = [
    {
      q: 'ما هو المصطلح الذي يُطلق على تطبيق يُستخدم عبر متصفح الويب؟',
      options: ['تطبيق سطح المكتب', 'تطبيق الويب', 'تطبيق الجوال الأصلي', 'نظام التشغيل'],
      answer: 1
    },
    {
      q: 'ما هو المصطلح الذي يُطلق على مكوّن الشاشة الذي يراه المستخدمون مباشرة؟',
      options: ['الواجهة الخلفية', 'قاعدة البيانات', 'الواجهة الأمامية', 'الخادم'],
      answer: 2
    },
    {
      q: 'ما هو المصطلح الذي يُطلق على الجزء المسؤول عن المعالجة من جانب الخادم؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'المتصفح', 'نظام الملفات'],
      answer: 1
    },
    {
      q: 'ما هو المصطلح الذي يُطلق على نظام ينظم البيانات ويخزنها ويديرها؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'قاعدة البيانات', 'نظام التشغيل'],
      answer: 2
    },
    {
      q: 'عند البحث عن منتج على موقع تسوق إلكتروني، أي جزء مسؤول عن البحث في البيانات عن المنتجات المطابقة؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'قاعدة البيانات', 'المتصفح فقط'],
      answer: 1
    },
    {
      q: 'صفحة عرض المنتجات تنتمي إلى أي طبقة؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'قاعدة البيانات'],
      answer: 0
    },
    {
      q: 'معالجة التحقق من المخزون تنتمي إلى أي طبقة؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'قاعدة البيانات'],
      answer: 1
    },
    {
      q: 'تخزين سجل الطلبات ينتمي إلى أي طبقة؟',
      options: ['الواجهة الأمامية', 'الواجهة الخلفية', 'قاعدة البيانات'],
      answer: 2
    }
  ];

  function renderQuiz() {
    let html = '';
    quizData.forEach((item, idx) => {
      html += `
        <div class="quiz-q" data-index="${idx}">
          <h6 class="mb-3"><span class="badge bg-primary me-2">${idx + 1}</span>${item.q}</h6>
          <div class="quiz-options">
            ${item.options.map((opt, oIdx) => `
              <label>
                <input type="radio" name="q${idx}" value="${oIdx}" class="me-2" />
                <span>${opt}</span>
              </label>
            `).join('')}
          </div>
        </div>
      `;
    });
    $('#quizContainer').html(html);
  }

  renderQuiz();

  $('#checkQuiz').on('click', function () {
    let correct = 0;
    quizData.forEach((item, idx) => {
      const $q = $(`.quiz-q[data-index="${idx}"]`);
      const selected = $q.find(`input[name="q${idx}"]:checked`).val();
      $q.removeClass('correct wrong');

      if (selected === undefined) {
        $q.addClass('wrong');
        return;
      }

      if (parseInt(selected) === item.answer) {
        $q.addClass('correct');
        correct++;
      } else {
        $q.addClass('wrong');
      }
    });

    const total = quizData.length;
    const percent = Math.round((correct / total) * 100);
    let msg = '';
    let alertClass = 'alert-danger';

    if (percent === 100) {
      msg = `ممتاز! أجبت على جميع الأسئلة بشكل صحيح (${correct}/${total}) 🎉`;
      alertClass = 'alert-success';
    } else if (percent >= 70) {
      msg = `جيد جدًا! أحرزت ${correct} من ${total} (${percent}%). راجع الإجابات الخاطئة.`;
      alertClass = 'alert-warning';
    } else {
      msg = `حصلت على ${correct} من ${total} (${percent}%). أعد قراءة الدرس ثم حاول مرة أخرى.`;
    }

    $('#quizResult')
      .removeClass('d-none')
      .html(`<div class="alert ${alertClass} text-center fs-5">${msg}</div>`);

    $('#resetQuiz').removeClass('d-none');
    $(this).addClass('d-none');
  });

  $('#resetQuiz').on('click', function () {
    renderQuiz();
    $('#quizResult').addClass('d-none').empty();
    $(this).addClass('d-none');
    $('#checkQuiz').removeClass('d-none');
  });

  // Video replay button
  $('#replayVideo').on('click', function () {
    const v = document.getElementById('layersVideo');
    if (v) {
      v.currentTime = 0;
      v.play();
    }
  });

  // Reveal answers in engineer section (fix for Bootstrap d-none)
  $('.reveal-btn').on('click', function () {
    const target = $(this).data('target');
    const $box = $('#' + target);
    const $btn = $(this);

    if ($box.hasClass('d-none') || !$box.is(':visible')) {
      $box.removeClass('d-none').hide().slideDown(350);
      $btn.html('<i class="fas fa-eye-slash me-1"></i> إخفاء الحل');
    } else {
      $box.slideUp(300, function () {
        $box.addClass('d-none');
      });
      $btn.html('<i class="fas fa-eye me-1"></i> أظهر نموذج الحل');
    }
  });

  // Intersection Observer for subtle entrance animations
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate__animated', 'animate__fadeInUp');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    document.querySelectorAll('.objective-card, .layer-detail-card, .challenge-card, .ex-item').forEach((el) => {
      observer.observe(el);
    });
  }
});
