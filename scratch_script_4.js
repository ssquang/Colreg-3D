
    const AudioEngine = {
      ctx: null,
      muted: false,
      init() {
        if (!this.ctx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) {
            this.ctx = new AudioContext();
          }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
          this.ctx.resume();
        }
      },
      playHorn(blasts = 1) {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;
        for (let i = 0; i < blasts; i++) {
          const startTime = this.ctx.currentTime + i * 1.1;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(140, startTime);
          osc.frequency.exponentialRampToValueAtTime(130, startTime + 0.8);
          gain.gain.setValueAtTime(0.0, startTime);
          gain.gain.linearRampToValueAtTime(0.35, startTime + 0.08);
          gain.gain.setValueAtTime(0.35, startTime + 0.7);
          gain.gain.linearRampToValueAtTime(0.001, startTime + 0.85);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(startTime);
          osc.stop(startTime + 0.85);
        }
      },
      playCrash() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const bufferSize = Math.floor(this.ctx.sampleRate * 1.2);
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(800, now);
        filter.frequency.linearRampToValueAtTime(120, now + 1.0);
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 1.2);
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);
        noise.start(now);

        const osc = this.ctx.createOscillator();
        const thumpGain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(95, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.8);
        thumpGain.gain.setValueAtTime(0.9, now);
        thumpGain.gain.exponentialRampToValueAtTime(0.01, now + 0.8);
        osc.connect(thumpGain);
        thumpGain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.8);
      },
      playChime() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const freqs = [523.25, 659.25, 783.99, 1046.50];
        freqs.forEach((f, idx) => {
          const t = now + idx * 0.12;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(f, t);
          gain.gain.setValueAtTime(0.0, t);
          gain.gain.linearRampToValueAtTime(0.25, t + 0.03);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.9);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(t);
          osc.stop(t + 0.9);
        });
      }
    };

    function toggleSound() {
      AudioEngine.muted = !AudioEngine.muted;
      document.getElementById('btnSoundToggle').textContent = AudioEngine.muted ? '🔇 Âm thanh: TẮT' : '🔊 Âm thanh: BẬT';
    }

    function triggerHorn(blasts) {
      AudioEngine.playHorn(blasts);
    }
  