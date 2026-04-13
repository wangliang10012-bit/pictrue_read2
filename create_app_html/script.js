function setRem() {
    const clientWidth = document.documentElement.clientWidth;
    document.documentElement.style.fontSize = (clientWidth / 375) * 16 + 'px';
}

setRem();
window.addEventListener('resize', setRem);

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

function updateRepaymentDate() {
    const dateEl = document.getElementById('nextRepaymentDate');
    if (dateEl) {
        dateEl.innerText = calculateNextRepaymentDate();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    updateRepaymentDate();
    setInterval(updateTime, 60000);
});

function navigateTo(page) {
    window.location.href = page;
}
