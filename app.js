/**
 * Dify 教學網站 - 主程式
 * 
 * 功能模組：
 * 1. 課程資料載入與管理
 * 2. Markdown 內容渲染
 * 3. 側邊欄導航控制
 * 4. 學習進度追蹤
 * 5. 學習計時器
 * 6. 主題切換
 * 7. localStorage 持久化
 */

// ==========================================================================
// 全域變數與設定
// ==========================================================================

/** 課程資料物件 */
let courseData = null;

/** 目前顯示的單元 ID */
let currentUnitId = null;

/** 所有單元的扁平列表（方便導航用） */
let flatUnits = [];

/** 學習進度資料 */
let progressData = {
    completedUnits: [],
    totalStudyTime: 0,
    todayStudyTime: 0,
    lastStudyDate: null,
    currentUnit: null
};

/** 計時器相關 */
let timerInterval = null;
let isPageVisible = true;

/** LocalStorage 鍵名 */
const STORAGE_KEYS = {
    PROGRESS: 'dify-tutorial-progress',
    THEME: 'dify-tutorial-theme'
};

// ==========================================================================
// 初始化
// ==========================================================================

/**
 * 頁面載入完成後執行初始化
 */
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // 載入主題設定
        initTheme();

        // 載入課程資料
        await loadCourseData();

        // 載入學習進度
        loadProgress();

        // 渲染側邊欄導航
        renderSidebar();

        // 渲染首頁課程預覽
        renderCourseOverview();

        // 初始化事件監聽
        initEventListeners();

        // 處理 URL hash 導航
        handleHashNavigation();

        // 啟動計時器
        startTimer();

        // 隱藏載入動畫
        hideLoader();

    } catch (error) {
        console.error('初始化失敗:', error);
        showToast('載入課程時發生錯誤', 'error');
        hideLoader();
    }
});

// ==========================================================================
// 課程資料載入
// ==========================================================================

/**
 * 載入課程資料（courses.json）
 * @returns {Promise<void>}
 */
async function loadCourseData() {
    const response = await fetch('courses.json');
    if (!response.ok) {
        throw new Error('無法載入課程資料');
    }
    courseData = await response.json();

    // 建立扁平單元列表（用於上下單元導航）
    flatUnits = [];
    courseData.chapters.forEach(chapter => {
        chapter.units.forEach(unit => {
            flatUnits.push({
                ...unit,
                chapterId: chapter.id,
                chapterTitle: chapter.title
            });
        });
    });
}

// ==========================================================================
// 側邊欄導航
// ==========================================================================

/**
 * 渲染側邊欄導航選單
 */
function renderSidebar() {
    const nav = document.getElementById('sidebarNav');
    if (!nav || !courseData) return;

    let html = '';

    courseData.chapters.forEach(chapter => {
        html += `
            <div class="nav-chapter" data-chapter="${chapter.id}">
                <div class="chapter-header" onclick="toggleChapter('${chapter.id}')">
                    <i class="${chapter.icon} chapter-icon"></i>
                    <span class="chapter-title">${chapter.title}</span>
                    <i class="fa-solid fa-chevron-down chapter-toggle"></i>
                </div>
                <div class="chapter-units">
        `;

        chapter.units.forEach(unit => {
            const isCompleted = progressData.completedUnits.includes(unit.id);
            const statusIcon = isCompleted
                ? '<i class="fa-solid fa-circle-check"></i>'
                : '<i class="fa-regular fa-circle"></i>';

            html += `
                <div class="nav-unit ${isCompleted ? 'completed' : ''}" 
                     data-unit="${unit.id}" 
                     onclick="navigateToUnit('${unit.id}')"
                     title="${unit.title}">
                    <span class="unit-status">${statusIcon}</span>
                    <span class="unit-title">${unit.title}</span>
                    <span class="unit-duration">${unit.duration}分</span>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    });

    nav.innerHTML = html;
    updateProgress();
}

/**
 * 展開/收合章節
 * @param {string} chapterId - 章節 ID
 */
function toggleChapter(chapterId) {
    const chapter = document.querySelector(`.nav-chapter[data-chapter="${chapterId}"]`);
    if (!chapter) return;

    const header = chapter.querySelector('.chapter-header');
    const units = chapter.querySelector('.chapter-units');

    header.classList.toggle('collapsed');
    units.classList.toggle('collapsed');
}

/**
 * 更新側邊欄中的目前單元高亮
 * @param {string} unitId - 單元 ID
 */
function updateActiveUnit(unitId) {
    // 移除所有 active 狀態
    document.querySelectorAll('.nav-unit').forEach(el => {
        el.classList.remove('active');
    });

    // 設定新的 active 狀態
    const activeUnit = document.querySelector(`.nav-unit[data-unit="${unitId}"]`);
    if (activeUnit) {
        activeUnit.classList.add('active');

        // 確保所屬章節展開
        const chapter = activeUnit.closest('.nav-chapter');
        if (chapter) {
            const header = chapter.querySelector('.chapter-header');
            const units = chapter.querySelector('.chapter-units');
            header.classList.remove('collapsed');
            units.classList.remove('collapsed');
        }
    }
}

// ==========================================================================
// 課程內容載入與顯示
// ==========================================================================

/**
 * 導航至指定單元
 * @param {string} unitId - 單元 ID
 */
async function navigateToUnit(unitId) {
    // 更新 URL hash
    window.location.hash = unitId;

    // 隱藏歡迎區，顯示內容區
    document.getElementById('welcomeSection').style.display = 'none';
    document.getElementById('contentSection').style.display = 'block';

    // 更新側邊欄高亮
    updateActiveUnit(unitId);

    // 載入內容
    await loadUnitContent(unitId);

    // 更新導航按鈕
    updateNavigationButtons(unitId);

    // 更新完成按鈕狀態
    updateCompleteButton(unitId);

    // 更新麵包屑
    updateBreadcrumb(unitId);

    // 儲存目前單元
    currentUnitId = unitId;
    progressData.currentUnit = unitId;
    saveProgress();

    // 捲動至頂部
    document.querySelector('.main-content').scrollTo(0, 0);

    // 關閉行動版選單
    closeMobileSidebar();
}

/**
 * 載入單元內容
 * @param {string} unitId - 單元 ID
 */
async function loadUnitContent(unitId) {
    const unit = flatUnits.find(u => u.id === unitId);
    if (!unit) {
        showContentError('找不到此單元');
        return;
    }

    // 更新標題區
    const chapterIndex = courseData.chapters.findIndex(c => c.id === unit.chapterId);
    document.getElementById('chapterBadge').textContent = `第 ${chapterIndex + 1} 章`;
    document.getElementById('durationBadge').querySelector('span').textContent = `${unit.duration} 分鐘`;
    document.getElementById('contentTitle').textContent = unit.title;

    const contentBody = document.getElementById('contentBody');
    contentBody.classList.add('loading');
    contentBody.innerHTML = '';

    try {
        // 檢查是否為 placeholder 單元
        if (unit.placeholder) {
            showPlaceholderContent(unit.title);
            return;
        }

        const response = await fetch(unit.contentPath);
        if (!response.ok) {
            throw new Error('無法載入內容');
        }

        const markdown = await response.text();

        // 使用 marked.js 渲染 Markdown
        const html = marked.parse(markdown, {
            gfm: true,
            breaks: true,
            headerIds: true
        });

        contentBody.innerHTML = html;
        contentBody.classList.remove('loading');
        contentBody.classList.add('animate-fadeIn');

        // 處理圖片路徑（相對於 contentPath）
        processContentImages(contentBody, unit.contentPath);

        // 高亮程式碼
        if (window.Prism) {
            Prism.highlightAllUnder(contentBody);
        }

        // 處理互動式小測驗
        processQuizzes(contentBody);

        // 移除動畫 class
        setTimeout(() => {
            contentBody.classList.remove('animate-fadeIn');
        }, 500);

    } catch (error) {
        console.error('載入內容失敗:', error);
        showPlaceholderContent(unit.title);
    }
}

/**
 * 處理內容中的圖片路徑
 * @param {HTMLElement} container - 內容容器
 * @param {string} contentPath - 內容檔案路徑
 */
function processContentImages(container, contentPath) {
    // 取得內容檔案的目錄路徑
    const basePath = contentPath.substring(0, contentPath.lastIndexOf('/') + 1);

    container.querySelectorAll('img').forEach(img => {
        const src = img.getAttribute('src');
        // 如果是相對路徑，轉換為完整路徑
        if (src && !src.startsWith('http') && !src.startsWith('/')) {
            img.setAttribute('src', basePath + src);
        }
    });
}

/**
 * 顯示 placeholder 內容（尚未完成的單元）
 * @param {string} title - 單元標題
 */
function showPlaceholderContent(title) {
    const contentBody = document.getElementById('contentBody');
    contentBody.classList.remove('loading');
    contentBody.classList.add('placeholder');
    contentBody.innerHTML = `
        <i class="fa-solid fa-file-circle-question"></i>
        <h2>內容準備中</h2>
        <p>「${title}」的課程內容正在編寫中，敬請期待！</p>
    `;
}

/**
 * 顯示內容載入錯誤
 * @param {string} message - 錯誤訊息
 */
function showContentError(message) {
    const contentBody = document.getElementById('contentBody');
    contentBody.classList.remove('loading');
    contentBody.classList.add('placeholder');
    contentBody.innerHTML = `
        <i class="fa-solid fa-triangle-exclamation"></i>
        <h2>載入失敗</h2>
        <p>${message}</p>
    `;
}

/**
 * 更新上一個/下一個導航按鈕
 * @param {string} unitId - 目前單元 ID
 */
function updateNavigationButtons(unitId) {
    const currentIndex = flatUnits.findIndex(u => u.id === unitId);

    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const prevTitle = document.getElementById('prevTitle');
    const nextTitle = document.getElementById('nextTitle');

    // 上一個
    if (currentIndex > 0) {
        const prevUnit = flatUnits[currentIndex - 1];
        prevBtn.disabled = false;
        prevTitle.textContent = prevUnit.title;
        prevBtn.onclick = () => navigateToUnit(prevUnit.id);
    } else {
        prevBtn.disabled = true;
        prevTitle.textContent = '-';
        prevBtn.onclick = null;
    }

    // 下一個
    if (currentIndex < flatUnits.length - 1) {
        const nextUnit = flatUnits[currentIndex + 1];
        nextBtn.disabled = false;
        nextTitle.textContent = nextUnit.title;
        nextBtn.onclick = () => navigateToUnit(nextUnit.id);
    } else {
        nextBtn.disabled = true;
        nextTitle.textContent = '-';
        nextBtn.onclick = null;
    }
}

/**
 * 更新完成按鈕狀態
 * @param {string} unitId - 單元 ID
 */
function updateCompleteButton(unitId) {
    const btn = document.getElementById('completeBtn');
    const isCompleted = progressData.completedUnits.includes(unitId);

    if (isCompleted) {
        btn.classList.add('completed');
        btn.innerHTML = '<i class="fa-solid fa-circle-check"></i><span>已完成</span>';
    } else {
        btn.classList.remove('completed');
        btn.innerHTML = '<i class="fa-regular fa-circle-check"></i><span>標記為已完成</span>';
    }
}

/**
 * 更新麵包屑
 * @param {string} unitId - 單元 ID
 */
function updateBreadcrumb(unitId) {
    const unit = flatUnits.find(u => u.id === unitId);
    if (!unit) return;

    const breadcrumb = document.getElementById('breadcrumb');
    breadcrumb.innerHTML = `
        <span class="breadcrumb-item" onclick="showWelcome()" style="cursor:pointer;">首頁</span>
        <span class="breadcrumb-separator"><i class="fa-solid fa-chevron-right"></i></span>
        <span class="breadcrumb-item">${unit.chapterTitle}</span>
        <span class="breadcrumb-separator"><i class="fa-solid fa-chevron-right"></i></span>
        <span class="breadcrumb-item">${unit.title}</span>
    `;
}

// ==========================================================================
// 首頁與歡迎區
// ==========================================================================

/**
 * 顯示歡迎區（首頁）
 */
function showWelcome() {
    window.location.hash = '';
    document.getElementById('welcomeSection').style.display = 'flex';
    document.getElementById('contentSection').style.display = 'none';

    // 更新麵包屑
    document.getElementById('breadcrumb').innerHTML = '<span class="breadcrumb-item">首頁</span>';

    // 移除側邊欄 active 狀態
    document.querySelectorAll('.nav-unit').forEach(el => {
        el.classList.remove('active');
    });

    currentUnitId = null;
}

/**
 * 渲染首頁課程預覽卡片
 */
function renderCourseOverview() {
    const container = document.getElementById('courseOverview');
    if (!container || !courseData) return;

    let html = '';

    courseData.chapters.forEach((chapter, index) => {
        const completedCount = chapter.units.filter(u =>
            progressData.completedUnits.includes(u.id)
        ).length;

        html += `
            <div class="overview-card" onclick="navigateToUnit('${chapter.units[0].id}')">
                <div class="overview-card-header">
                    <div class="overview-card-icon">
                        <i class="${chapter.icon}"></i>
                    </div>
                    <div class="overview-card-title">
                        <h3>第 ${index + 1} 章：${chapter.title}</h3>
                        <p>${chapter.subtitle || ''}</p>
                    </div>
                </div>
                <div class="overview-card-meta">
                    <span><i class="fa-solid fa-file-lines"></i> ${chapter.units.length} 單元</span>
                    <span><i class="fa-regular fa-clock"></i> ${chapter.duration} 分鐘</span>
                    <span><i class="fa-solid fa-check-circle"></i> ${completedCount}/${chapter.units.length}</span>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// ==========================================================================
// 進度追蹤
// ==========================================================================

/**
 * 從 localStorage 載入學習進度
 */
function loadProgress() {
    try {
        const saved = localStorage.getItem(STORAGE_KEYS.PROGRESS);
        if (saved) {
            const data = JSON.parse(saved);
            progressData = { ...progressData, ...data };

            // 檢查是否為新的一天，重設今日學習時間
            const today = new Date().toISOString().split('T')[0];
            if (progressData.lastStudyDate !== today) {
                progressData.todayStudyTime = 0;
                progressData.lastStudyDate = today;
            }
        }
    } catch (error) {
        console.error('載入進度失敗:', error);
    }
}

/**
 * 儲存學習進度至 localStorage
 */
function saveProgress() {
    try {
        progressData.lastStudyDate = new Date().toISOString().split('T')[0];
        localStorage.setItem(STORAGE_KEYS.PROGRESS, JSON.stringify(progressData));
    } catch (error) {
        console.error('儲存進度失敗:', error);
    }
}

/**
 * 更新進度顯示
 */
function updateProgress() {
    const totalUnits = flatUnits.length;
    const completedUnits = progressData.completedUnits.length;
    const percentage = totalUnits > 0 ? Math.round((completedUnits / totalUnits) * 100) : 0;

    // 更新進度條
    document.getElementById('progressPercentage').textContent = `${percentage}%`;
    document.getElementById('progressFill').style.width = `${percentage}%`;
}

/**
 * 切換單元完成狀態
 */
function toggleUnitComplete() {
    if (!currentUnitId) return;

    const index = progressData.completedUnits.indexOf(currentUnitId);

    if (index > -1) {
        // 取消完成
        progressData.completedUnits.splice(index, 1);
        showToast('已取消完成標記', 'success');
    } else {
        // 標記完成
        progressData.completedUnits.push(currentUnitId);
        showToast('已標記為完成！', 'success');
    }

    // 更新 UI
    updateCompleteButton(currentUnitId);
    updateSidebarUnitStatus(currentUnitId);
    updateProgress();
    renderCourseOverview();
    saveProgress();
}

/**
 * 更新側邊欄單元完成狀態
 * @param {string} unitId - 單元 ID
 */
function updateSidebarUnitStatus(unitId) {
    const unitEl = document.querySelector(`.nav-unit[data-unit="${unitId}"]`);
    if (!unitEl) return;

    const isCompleted = progressData.completedUnits.includes(unitId);
    const statusEl = unitEl.querySelector('.unit-status');

    if (isCompleted) {
        unitEl.classList.add('completed');
        statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
    } else {
        unitEl.classList.remove('completed');
        statusEl.innerHTML = '<i class="fa-regular fa-circle"></i>';
    }
}

// ==========================================================================
// 學習計時器
// ==========================================================================

/**
 * 啟動學習計時器
 */
function startTimer() {
    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (!isPageVisible) return;

        progressData.totalStudyTime++;
        progressData.todayStudyTime++;

        updateTimerDisplay();

        // 每 30 秒儲存一次進度
        if (progressData.totalStudyTime % 30 === 0) {
            saveProgress();
        }
    }, 1000);
}

/**
 * 更新計時器顯示
 */
function updateTimerDisplay() {
    document.getElementById('todayTimer').textContent = formatTime(progressData.todayStudyTime);
    document.getElementById('totalTimer').textContent = formatTime(progressData.totalStudyTime);
}

/**
 * 格式化時間（秒轉為 HH:MM:SS）
 * @param {number} seconds - 秒數
 * @returns {string} 格式化後的時間字串
 */
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return [hours, minutes, secs]
        .map(n => n.toString().padStart(2, '0'))
        .join(':');
}

// ==========================================================================
// 主題切換
// ==========================================================================

/**
 * 初始化主題
 */
function initTheme() {
    const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME) || 'dark';
    setTheme(savedTheme);
}

/**
 * 設定主題
 * @param {string} theme - 'dark' 或 'light'
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'dark'
            ? '<i class="fa-solid fa-moon"></i>'
            : '<i class="fa-solid fa-sun"></i>';
    }

    localStorage.setItem(STORAGE_KEYS.THEME, theme);
}

/**
 * 切換主題
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// ==========================================================================
// 事件監聽
// ==========================================================================

/**
 * 初始化所有事件監聽器
 */
function initEventListeners() {
    // 主題切換
    document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);

    // 完成按鈕
    document.getElementById('completeBtn')?.addEventListener('click', toggleUnitComplete);

    // 開始學習按鈕
    document.getElementById('startLearningBtn')?.addEventListener('click', () => {
        // 如果有上次閱讀的單元，跳轉到該單元，否則跳轉到第一個單元
        const targetUnit = progressData.currentUnit || (flatUnits[0]?.id);
        if (targetUnit) {
            navigateToUnit(targetUnit);
        }
    });

    // 側邊欄收合（桌面版）
    document.getElementById('sidebarToggle')?.addEventListener('click', () => {
        document.getElementById('sidebar')?.classList.toggle('collapsed');
    });

    // 側邊欄展開按鈕（收合後顯示）
    document.getElementById('sidebarExpandBtn')?.addEventListener('click', () => {
        document.getElementById('sidebar')?.classList.remove('collapsed');
    });

    // 行動版選單
    document.getElementById('mobileMenuBtn')?.addEventListener('click', openMobileSidebar);
    document.getElementById('sidebarOverlay')?.addEventListener('click', closeMobileSidebar);

    // URL hash 變更
    window.addEventListener('hashchange', handleHashNavigation);

    // 頁面可見性變更（用於暫停計時器）
    document.addEventListener('visibilitychange', () => {
        isPageVisible = !document.hidden;
    });

    // 捲動事件（返回頂部按鈕）
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.addEventListener('scroll', handleScroll);
    }

    // 返回頂部按鈕
    document.getElementById('backToTop')?.addEventListener('click', () => {
        document.querySelector('.main-content').scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 鍵盤導航
    document.addEventListener('keydown', handleKeyNavigation);
}

/**
 * 處理 URL hash 導航
 */
function handleHashNavigation() {
    const hash = window.location.hash.slice(1);

    if (hash && flatUnits.some(u => u.id === hash)) {
        navigateToUnit(hash);
    } else {
        showWelcome();
    }
}

/**
 * 處理捲動事件
 * @param {Event} event - 捲動事件
 */
function handleScroll(event) {
    const scrollTop = event.target.scrollTop;
    const backToTop = document.getElementById('backToTop');

    if (backToTop) {
        if (scrollTop > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }
}

/**
 * 處理鍵盤導航
 * @param {KeyboardEvent} event - 鍵盤事件
 */
function handleKeyNavigation(event) {
    // 只在內容區有焦點時處理
    if (!currentUnitId) return;

    const currentIndex = flatUnits.findIndex(u => u.id === currentUnitId);

    switch (event.key) {
        case 'ArrowLeft':
            // 上一個單元
            if (currentIndex > 0) {
                navigateToUnit(flatUnits[currentIndex - 1].id);
            }
            break;
        case 'ArrowRight':
            // 下一個單元
            if (currentIndex < flatUnits.length - 1) {
                navigateToUnit(flatUnits[currentIndex + 1].id);
            }
            break;
    }
}

// ==========================================================================
// 行動版側邊欄
// ==========================================================================

/**
 * 開啟行動版側邊欄
 */
function openMobileSidebar() {
    document.getElementById('sidebar')?.classList.add('active');
    document.getElementById('sidebarOverlay')?.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * 關閉行動版側邊欄
 */
function closeMobileSidebar() {
    document.getElementById('sidebar')?.classList.remove('active');
    document.getElementById('sidebarOverlay')?.classList.remove('active');
    document.body.style.overflow = '';
}

// ==========================================================================
// 工具函式
// ==========================================================================

/**
 * 隱藏載入動畫
 */
function hideLoader() {
    document.getElementById('loader')?.classList.add('hidden');
}

/**
 * 顯示 Toast 通知
 * @param {string} message - 訊息內容
 * @param {string} type - 類型 ('success' | 'error')
 */
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // 3 秒後移除
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==========================================================================
// 互動式小測驗處理
// ==========================================================================

/**
 * 處理內容中的小測驗區塊
 * 將 [!QUIZ] 格式的測驗轉換為互動式選項，需點選後才顯示答案
 * @param {HTMLElement} container - 內容容器
 */
function processQuizzes(container) {
    // 尋找所有 blockquote 元素
    const blockquotes = container.querySelectorAll('blockquote');

    blockquotes.forEach(blockquote => {
        // 檢查是否為小測驗區塊（包含 [!QUIZ] 文字）
        const text = blockquote.textContent;
        if (!text.includes('[!QUIZ]')) return;

        // 標記為小測驗區塊
        blockquote.classList.add('quiz-block');

        // 移除 [!QUIZ] 標記
        const html = blockquote.innerHTML;
        blockquote.innerHTML = html.replace('[!QUIZ]', '');

        // 找出所有選項（li 元素或使用 checkbox 格式的行）
        const listItems = blockquote.querySelectorAll('li');

        if (listItems.length > 0) {
            // 使用 ul/ol 格式
            listItems.forEach(li => {
                processQuizOption(li, blockquote);
            });
        } else {
            // 可能使用純文字格式，尋找 [ ] 和 [x] 模式
            const paragraphs = blockquote.querySelectorAll('p');
            paragraphs.forEach(p => {
                const content = p.innerHTML;
                // 檢查是否包含選項格式 - [ ] 或 - [x]
                if (content.includes('- [ ]') || content.includes('- [x]')) {
                    processTextQuizOptions(p, blockquote);
                }
            });
        }

        // 加入「點選查看答案」提示
        if (!blockquote.querySelector('.quiz-hint')) {
            const hint = document.createElement('div');
            hint.className = 'quiz-hint';
            hint.innerHTML = '<i class="fa-solid fa-lightbulb"></i> 點選選項查看答案';
            blockquote.appendChild(hint);
        }
    });
}

/**
 * 處理 li 格式的小測驗選項
 * marked.js 會將 - [x] 渲染為 <input type="checkbox" checked>
 * @param {HTMLElement} li - 列表項目元素
 * @param {HTMLElement} quizBlock - 小測驗區塊
 */
function processQuizOption(li, quizBlock) {
    // 找出 checkbox 元素來判斷正確答案
    const checkbox = li.querySelector('input[type="checkbox"]');
    const isCorrect = checkbox ? checkbox.checked : false;

    // 取得選項文字內容（移除 checkbox 後）
    let cleanContent = '';
    if (checkbox) {
        // 先移除 checkbox
        checkbox.remove();
        cleanContent = li.innerHTML.trim();
    } else {
        // 如果沒有 checkbox，用文字判斷
        const content = li.innerHTML;
        const hasChecked = content.includes('[x]') || content.includes('☑');
        cleanContent = content
            .replace(/\[x\]/gi, '')
            .replace(/\[ \]/gi, '')
            .replace(/☑/g, '')
            .replace(/☐/g, '')
            .trim();
    }

    // 建立可點選的選項
    li.innerHTML = `<span class="quiz-option ${isCorrect ? 'correct' : 'incorrect'}">${cleanContent}</span>`;
    li.classList.add('quiz-item');

    // 綁定點選事件
    const option = li.querySelector('.quiz-option');
    option.addEventListener('click', () => {
        handleQuizOptionClick(option, quizBlock);
    });
}

/**
 * 處理純文字格式的小測驗選項
 * @param {HTMLElement} paragraph - 段落元素
 * @param {HTMLElement} quizBlock - 小測驗區塊
 */
function processTextQuizOptions(paragraph, quizBlock) {
    const content = paragraph.innerHTML;
    const lines = content.split('<br>');

    let newContent = '';
    lines.forEach(line => {
        if (line.includes('- [ ]') || line.includes('- [x]')) {
            const isCorrect = line.includes('- [x]');
            const cleanLine = line
                .replace('- [x]', '')
                .replace('- [ ]', '')
                .trim();

            newContent += `<div class="quiz-item"><span class="quiz-option ${isCorrect ? 'correct' : 'incorrect'}">${cleanLine}</span></div>`;
        } else {
            newContent += line + '<br>';
        }
    });

    paragraph.innerHTML = newContent;

    // 綁定點選事件
    const options = paragraph.querySelectorAll('.quiz-option');
    options.forEach(option => {
        option.addEventListener('click', () => {
            handleQuizOptionClick(option, quizBlock);
        });
    });
}

/**
 * 處理小測驗選項點選事件
 * @param {HTMLElement} option - 被點選的選項
 * @param {HTMLElement} quizBlock - 小測驗區塊
 */
function handleQuizOptionClick(option, quizBlock) {
    // 檢查是否已經揭曉答案
    if (quizBlock.classList.contains('revealed')) {
        return;
    }

    // 標記區塊為已揭曉
    quizBlock.classList.add('revealed');

    // 顯示所有選項的正確/錯誤狀態
    const allOptions = quizBlock.querySelectorAll('.quiz-option');
    allOptions.forEach(opt => {
        opt.classList.add('show-result');
    });

    // 標記使用者選擇的選項
    option.classList.add('selected');

    // 隱藏提示文字
    const hint = quizBlock.querySelector('.quiz-hint');
    if (hint) {
        hint.style.display = 'none';
    }

    // 顯示結果訊息
    const isCorrect = option.classList.contains('correct');
    const resultMsg = document.createElement('div');
    resultMsg.className = `quiz-result ${isCorrect ? 'correct' : 'incorrect'}`;
    resultMsg.innerHTML = isCorrect
        ? '<i class="fa-solid fa-circle-check"></i> 答對了！'
        : '<i class="fa-solid fa-circle-xmark"></i> 答錯了，正確答案已標示';
    quizBlock.appendChild(resultMsg);
}

// ==========================================================================
// 頁面卸載前儲存進度
// ==========================================================================

window.addEventListener('beforeunload', () => {
    saveProgress();
});

