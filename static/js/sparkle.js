window.addEventListener("DOMContentLoaded", () => {
    const starsContainer = document.querySelector(".stars");
    if (!starsContainer) return;

    const createStar = () => {
        const starEl = document.createElement("span");
        starEl.className = "star";

        // サイズを1px〜3pxの間でランダムに（少しだけ大きくして目立たせる）
        const size = Math.random() * 2 + 1;
        starEl.style.width = `${size}px`;
        starEl.style.height = `${size}px`;

        // 配置場所をランダムに
        starEl.style.left = `${Math.random() * 100}%`;
        starEl.style.top = `${Math.random() * 100}%`;

        // 💡 点滅のタイミング（Delay）と、光っている時間（Duration）をバラバラにする
        // これで「一斉に光って一斉に消える」のを防ぎ、自然な星空になります
        starEl.style.animationDelay = `${Math.random() * 10}s`;
        starEl.style.animationDuration = `${Math.random() * 5 + 3}s`;

        starsContainer.appendChild(starEl);
    };

    // 500個の星を生成
    for (let i = 0; i <= 500; i++) {
        createStar();
    }
});