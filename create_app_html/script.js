function setRem() {
    const clientWidth = document.documentElement.clientWidth;
    document.documentElement.style.fontSize = (clientWidth / 375) * 16 + 'px';
}

setRem();
window.addEventListener('resize', setRem);

// 简化版底部适配：仅确保最后一个元素没有多余间距
function forceBottomStick() {
    if (!document.body.classList.contains('index-page')) {
        return;
    }
    const containers = document.querySelectorAll('.image-container');
    if (containers.length > 0) {
        const lastContainer = containers[containers.length - 1];
        lastContainer.style.marginTop = '0';
        lastContainer.style.marginBottom = '0';
    }
}

// 页面加载完成后执行
window.addEventListener('load', function() {
    setTimeout(forceBottomStick, 100);
});

// 窗口大小变化时重新计算
window.addEventListener('resize', function() {
    setTimeout(forceBottomStick, 100);
});

function calculateNextRepaymentDate() {
    const today = new Date();
    const currentDay = today.getDate();
    let nextMonth = today.getMonth() + 1;
    let nextYear = today.getFullYear();

    if (currentDay >= 27) {
        nextMonth += 1;
        if (nextMonth > 12) {
            nextMonth = 1;
            nextYear += 1;
        }
    }

    return nextYear + "-" + String(nextMonth).padStart(2, '0') + "-27";
}

function updateTime() {
    const now = new Date();
    const timeString = now.getFullYear() + "-" +
        String(now.getMonth() + 1).padStart(2, '0') + "-" +
        String(now.getDate()).padStart(2, '0') + " " +
        String(now.getHours()).padStart(2, '0') + ":" +
        String(now.getMinutes()).padStart(2, '0') + ":" +
        String(now.getSeconds()).padStart(2, '0');

    const loginTimeEl = document.getElementById('loginTime');
    if (loginTimeEl) {
        loginTimeEl.innerText = "上次登录 " + timeString;
    }
}

// 更新资产负债卡片中的时间
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.getFullYear() + "-" +
        String(now.getMonth() + 1).padStart(2, '0') + "-" +
        String(now.getDate()).padStart(2, '0') + " " +
        String(now.getHours()).padStart(2, '0') + ":" +
        String(now.getMinutes()).padStart(2, '0') + ":" +
        String(now.getSeconds()).padStart(2, '0');

    const currentTimeEl = document.getElementById('currentTime');
    if (currentTimeEl) {
        currentTimeEl.innerText = "时间 " + timeString;
    }
}

function updateRepaymentDate() {
    const dateEl = document.getElementById('nextRepaymentDate');
    if (dateEl) {
        dateEl.innerText = calculateNextRepaymentDate();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    updateCurrentTime();
    updateRepaymentDate();
    setInterval(updateTime, 60000);
    setInterval(updateCurrentTime, 60000);
});

function navigateTo(page) {
    window.location.href = page;
}
