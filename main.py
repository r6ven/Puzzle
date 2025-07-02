<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
  <title>50 Parçalı Puzzle Oyunu</title>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3/dist/phaser.min.js"></script>
  <style>
    body { margin: 0; overflow: hidden; }
    #congrats {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%) scale(0.5);
      opacity: 0;
      font-size: 2rem;
      color: #fff;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
      pointer-events: none;
      z-index: 10;
    }
    .show {
      animation: showAnim 1s forwards;
    }
    @keyframes showAnim {
      0%   { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
      60%  { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
      100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    }
  </style>
</head>
<body>
  <div id="congrats">Seni çok seviyorum 💖</div>
  <script>
    const config = {
      type: Phaser.AUTO,
      width: 360,
      height: 640,
      backgroundColor: '#333',
      parent: document.body,
      scene: { preload, create }
    };
    new Phaser.Game(config);

    function preload() {
      // Tek bir büyük puzzle görseli yükleyin (örn: assets/puzzle.jpg)
      this.load.image('puzzle', 'assets/puzzle.jpg');
    }

    function create() {
      const img = this.textures.get('puzzle').getSourceImage();
      const cols = 10, rows = 5;
      const pw = img.width / cols, ph = img.height / rows;
      const pieces = [];

      // Parçaları dinamik olarak kırpıp dokuya ekleme
      let idx = 0;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          // Canvas oluştur
          const cv = document.createElement('canvas');
          cv.width = pw; cv.height = ph;
          const ctx = cv.getContext('2d');
          ctx.drawImage(img,
            c * pw, r * ph, pw, ph,
            0, 0, pw, ph
          );
          // Phaser texture olarak ekle
          this.textures.addCanvas('piece' + idx, cv);

          // Rastgele pozisyona yerleştir
          const x = Phaser.Math.Between(pw/2, config.width - pw/2);
          const y = Phaser.Math.Between(ph/2, config.height - ph/2);
          const spr = this.add.image(x, y, 'piece' + idx).setInteractive();
          this.input.setDraggable(spr);

          pieces.push({ spr, correctX: c * pw + pw/2, correctY: r * ph + ph/2 });
          idx++;
        }
      }

      // Sürükle bırak işlemleri
      this.input.on('drag', (pointer, gameObject, dragX, dragY) => {
        gameObject.x = dragX;
        gameObject.y = dragY;
      });
      this.input.on('dragend', () => checkDone(this, pieces));
    }

    function checkDone(scene, pieces) {
      const done = pieces.every(p => Phaser.Math.Distance.Between(
        p.spr.x, p.spr.y,
        p.correctX, p.correctY
      ) < 20);
      if (done) showCongrats();
    }

    function showCongrats() {
      document.getElementById('congrats').classList.add('show');
    }
  </script>
</body>
</html>
