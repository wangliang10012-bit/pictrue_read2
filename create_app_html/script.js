function setRem() {
    const clientWidth = document.documentElement.clientWidth;
    document.documentElement.style.fontSize = (clientWidth / 375) * 16 + 'px';
}

setRem();
window.addEventListener('resize', setRem);

// 强制底部导航贴底
function forceBottomStick() {
    // 只在 index.html 页面执行
    if (!document.body.classList.contains('index-page')) {
        return;
    }

    // 获取视口高度
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    
    // 获取所有 image-container
    const containers = document.querySelectorAll('.image-container');
    if (containers.length === 0) return;
    
    // 获取最后一个容器（底部导航）
    const lastContainer = containers[containers.length - 1];
    
    // 计算前面所有容器的总高度
    let totalHeight = 0;
    for (let i = 0; i < containers.length - 1; i++) {
        totalHeight += containers[i].offsetHeight;
        // 加上 margin-bottom (0.5vh)
        const marginBottom = viewportHeight * 0.005;
        totalHeight += marginBottom;
    }
    
    // 计算剩余空间
    const remainingSpace = viewportHeight - totalHeight - lastContainer.offsetHeight;
    
    // 如果还有剩余空间，给最后一个容器添加 margin-top
    if (remainingSpace > 0) {
        lastContainer.style.marginTop = `${remainingSpace}px`;
        console.log(`视口高度: ${viewportHeight}, 内容高度: ${totalHeight + lastContainer.offsetHeight}, 剩余空间: ${remainingSpace}`);
    } else {
        lastContainer.style.marginTop = '0';
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

// 图片加载完成后也执行
window.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    let loadedCount = 0;
    
    images.forEach(img => {
        if (img.complete) {
            loadedCount++;
        } else {
            img.addEventListener('load', () => {
                loadedCount++;
                if (loadedCount === images.length) {
                    setTimeout(forceBottomStick, 50);
                }
            });
        }
    });
    
    if (loadedCount === images.length) {
        setTimeout(forceBottomStick, 50);
    }
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
