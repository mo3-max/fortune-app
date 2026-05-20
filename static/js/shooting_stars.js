document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('shooting-stars');
    if (!container) return;

    // 流れ星を1本作成する関数
    function createShootingStar() {
        const star = document.createElement('div');
        star.className = 'shooting-star';

        // 💡 画面の右側・上側のランダムな位置からスタート
        const startX = Math.random() * (window.innerWidth * 0.5) + (window.innerWidth * 0.4);
        const startY = Math.random() * (window.innerHeight * 0.3);

        star.style.left = startX + 'px';
        star.style.top = startY + 'px';

        // 💡 流れるスピードをランダムに (1秒〜1.8秒の間でスッと流れる)
        const duration = Math.random() * 800 + 1000;
        star.style.animationDuration = duration + 'ms';

        container.appendChild(star);

        // 流れ終わったら画面から消去（お掃除）
        setTimeout(() => {
            star.remove();
        }, duration);
    }

    // 💡 定期的に流れ星を発生させる（3秒〜7秒に1回、ランダムな間隔で流れる）
    function startShooting() {
        const nextDelay = Math.random() * 4000 + 3000;
        setTimeout(() => {
            createShootingStar();
            startShooting(); // 次の流れ星を予約
        }, nextDelay);
    }

    // 画面が開いて2秒後に最初の流れ星をスタート
    setTimeout(createShootingStar, 2000);
    startShooting();
});