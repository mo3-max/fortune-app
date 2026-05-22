// 🌌 画面の読み込みが完了した時の処理
$(window).on('load', function () {

    // 1️⃣ 【最上部へスクロール】
    // 画面が100%完全に読み込み終わったら一番上へ弾く（少し余裕を持たせて100ミリ秒後に実行）
    setTimeout(function () {
        window.scrollTo(0, 0);
    }, 100);

    // 2️⃣ 【文字色を変える魔法】
    // 各要素が持つ「data-color」の値を読み取って、自分自身の文字色（color）に自動反映
    $('.shugoshin-highlight').css('color', function () {
        return $(this).data('color');
    });

});