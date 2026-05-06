const config = {
    type: Phaser.AUTO,
    width: 1024,
    height: 680,
    parent: "phaser-game",
    backgroundColor: '#0a0a0a',
    physics: {
        default: 'arcade',
        arcade: { gravity: { y: 0 }, debug: false }
    },
    scene: [LobbyScene, GameScene]
};

const game = new Phaser.Game(config);

// ==================== LOBBY ====================
class LobbyScene extends Phaser.Scene {
    constructor() { super({ key: 'LobbyScene' }); }

    create() {
        this.add.rectangle(512, 340, 1024, 680, 0x1a1a2e);
        this.add.text(512, 80, "მთის წყევლა", { fontSize: '48px', fontStyle: 'bold', color: '#ff3333' }).setOrigin(0.5);
        this.add.text(512, 140, "BATTLE ROYALE", { fontSize: '28px', color: '#ffaa00' }).setOrigin(0.5);

        this.add.text(180, 220, "რუმი: #GE-7482", { fontSize: '24px', color: '#fff' });
        this.add.text(180, 260, "რეჟიმი: Solo", { fontSize: '24px', color: '#00ff88' });
        this.add.text(180, 300, "მოთამაშეები: 1 / 100", { fontSize: '24px', color: '#ffff00' });

        const readyBtn = this.add.rectangle(512, 480, 360, 90, 0x00aa00)
            .setInteractive({ useHandCursor: true })
            .on('pointerdown', () => this.scene.start('GameScene'));

        this.add.text(512, 480, "მზადაა (Ready)", { fontSize: '34px', color: '#ffffff', fontStyle: 'bold' }).setOrigin(0.5);
    }
}

// ==================== GAME SCENE ====================
class GameScene extends Phaser.Scene {
    constructor() {
        super({ key: 'GameScene' });
    }

    preload() {
        this.load.spritesheet('player', 'assets/sprites/player.png', { 
            frameWidth: 32, 
            frameHeight: 48 
        });
    }

    create() {
        this.add.rectangle(512, 340, 3000, 3000, 0x1e3a2f);

        this.player = this.physics.add.sprite(512, 340, 'player');
        this.player.setCollideWorldBounds(true);

        this.createAnimations();

        this.cursors = this.input.keyboard.createCursorKeys();
        this.keys = this.input.keyboard.addKeys('W,A,S,D');

        // UI
        this.add.text(20, 20, "მთის წყევლა", { fontSize: '26px', color: '#ff0000' });
        this.hpText = this.add.text(20, 55, "HP: 100", { fontSize: '20px', color: '#00ff00' });
    }

    createAnimations() {
        // Idle
        this.anims.create({ key: 'idle-down', frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }), frameRate: 8, repeat: -1 });
        this.anims.create({ key: 'idle-up', frames: this.anims.generateFrameNumbers('player', { start: 8, end: 11 }), frameRate: 8, repeat: -1 });
        this.anims.create({ key: 'idle-left', frames: this.anims.generateFrameNumbers('player', { start: 12, end: 15 }), frameRate: 8, repeat: -1 });
        this.anims.create({ key: 'idle-right', frames: this.anims.generateFrameNumbers('player', { start: 4, end: 7 }), frameRate: 8, repeat: -1 });

        // Walk
        this.anims.create({ key: 'walk-down', frames: this.anims.generateFrameNumbers('player', { start: 16, end: 23 }), frameRate: 12, repeat: -1 });
        this.anims.create({ key: 'walk-up', frames: this.anims.generateFrameNumbers('player', { start: 24, end: 31 }), frameRate: 12, repeat: -1 });
        this.anims.create({ key: 'walk-left', frames: this.anims.generateFrameNumbers('player', { start: 32, end: 39 }), frameRate: 12, repeat: -1 });
        this.anims.create({ key: 'walk-right', frames: this.anims.generateFrameNumbers('player', { start: 40, end: 47 }), frameRate: 12, repeat: -1 });
    }

    update() {
        const speed = 170;
        this.player.setVelocity(0);

        let moving = false;
        let direction = 'down';

        if (this.cursors.left.isDown || this.keys.A.isDown) { 
            this.player.setVelocityX(-speed); 
            direction = 'left'; 
            moving = true; 
        }
        if (this.cursors.right.isDown || this.keys.D.isDown) { 
            this.player.setVelocityX(speed); 
            direction = 'right'; 
            moving = true; 
        }
        if (this.cursors.up.isDown || this.keys.W.isDown) { 
            this.player.setVelocityY(-speed); 
            direction = 'up'; 
            moving = true; 
        }
        if (this.cursors.down.isDown || this.keys.S.isDown) { 
            this.player.setVelocityY(speed); 
            direction = 'down'; 
            moving = true; 
        }

        // ანიმაციის დაკვრა
        if (moving) {
            this.player.anims.play(`walk-${direction}`, true);
        } else {
            this.player.anims.play(`idle-${direction}`, true);
        }
    }
}
