// 🌌 夜空にロマンチックな流れ星を降らせる演出
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('shooting-stars');
    if (!container) return;

    // 🌟 流れ星を1本作成する関数
    function createShootingStar() {
        const star = document.createElement('div');
        star.className = 'shooting-star';

        // 💡 どの画面サイズでも綺麗に収まるよう、パーセンテージ(%)で出現位置を計算
        // 画面の右側（40%〜90%）× 上側（0%〜30%）のエリアからスタート
        const startX = Math.random() * 50 + 40;
        const startY = Math.random() * 30;

        star.style.left = startX + '%';
        star.style.top = startY + '%';

        // 💡 流れるスピードをランダムに (1秒〜1.8秒の間でスッと流れる)
        const duration = Math.random() * 800 + 1000;
        star.style.animationDuration = duration + 'ms';

        container.appendChild(star);

        // 流れ終わったら画面から消去（完全にアニメーションが終わってからお掃除）
        setTimeout(() => {
            star.remove();
        }, duration + 50);
    }

    // 💡 定期的に流れ星を発生させる（3秒〜7秒に1回、ランダムな間隔でループ）
    function startShooting() {
        // 次に流れるまでの待ち時間をランダムに決定
        const nextDelay = Math.random() * 4000 + 3000;

        setTimeout(() => {
            createShootingStar();
            startShooting(); // 次の流れ星を自動で予約（ループ）
        }, nextDelay);
    }

    // 画面が開いて2秒後に、最初の流れ星のループシステムを起動
    setTimeout(() => {
        createShootingStar(); // 最初の1本をスッと流す
        startShooting();      // 以降、定期的なランダム発生を開始
    }, 2000);
});