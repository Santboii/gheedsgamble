# 🎲 Gheed's Gamble

> *"Good day to you partner!"* - Gheed

Welcome to **Gheed's Gamble** - the ultimate Diablo 2: Resurrected hardcore randomizer! Spin the wheel of fate and let RNG decide your class, build, and challenges. Will you survive Sanctuary, or will you become another soul for the Burning Hells?

🌐 **Live Site:** [gheedsgamble.com](https://gheedsgamble.com)

---

## 🔥 Features

### 🎰 Wheel of Fate
- **Spin to Win (or Die)**: Beautiful animated roulette wheel powered by `react-custom-roulette`
- **Dagger Pointer**: A flickering dagger points to your destiny
- **Smooth Animations**: Flame effects, blood splatters, and dark Diablo aesthetics

### 🎮 Randomization System
- **7 Classes**: Amazon, Assassin, Necromancer, Barbarian, Paladin, Sorceress, Druid
- **48+ Builds**: Multiple viable builds per class with skill descriptions
- **20 Challenges**: From "No Runewords" to "Glass Cannon" - test your limits!
- **Weighted Selection**: Challenges have different probabilities for balanced difficulty

### ⚙️ Configuration
- **Rerolls**: Set how many times you can defy fate (0-10)
- **Challenge Count**: Choose 0-5 challenges with thematic names:
  - None (Coward)
  - 1 (Cautious)
  - 2 (Brave)
  - 3 (Reckless)
  - 4 (Insane)
  - 5 (Death Wish)

### 📊 Run Tracking
- **Save Runs**: Track your attempts with localStorage
- **Status Management**: Mark runs as Active, Completed, or Failed
- **History View**: Review all your past runs
- **Export/Import**: Backup your run history as JSON
- **Persistent Storage**: Your data survives browser restarts

---

## 🚀 Tech Stack

- **Framework**: [Next.js 16](https://nextjs.org/) with App Router
- **Language**: TypeScript
- **Styling**: Vanilla CSS (CSS Modules)
- **Wheel**: [react-custom-roulette](https://www.npmjs.com/package/react-custom-roulette)
- **Storage**: Browser localStorage
- **Deployment**: Vercel

---

## 🛠️ Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/santboii/gheedsgamble.git
cd gheedsgamble

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

### Build for Production

```bash
npm run build
npm start
```

---

## 📁 Project Structure

```
src/
├── app/
│   ├── page.tsx           # Main application logic
│   ├── page.module.css    # Page-specific styles
│   ├── globals.css        # Global styles & animations
│   └── layout.tsx         # Root layout
├── components/
│   ├── Wheel.tsx          # Roulette wheel component
│   └── Wheel.module.css   # Wheel styles
├── data.ts                # Classes, builds, challenges data
└── utils/
    └── runStorage.ts      # localStorage utilities

public/
├── background.png         # Dark Sanctuary background
├── dagger.png            # Wheel pointer
├── fire_strip.png        # Flame animation sprite
└── skeletal_hand.png     # Alternative pointer
```

---

## 🎨 Features Deep Dive

### Challenge Types

**Equipment Restrictions:**
- No Runewords
- No Unique/Rare/Set Items
- No Charms
- No Crafting

**Gameplay Modifiers:**
- Glass Cannon (no defensive stats)
- No Synergies
- No Mercenary
- Pacifist (Thorns/Auras only)

**Movement & Resources:**
- No Waypoints
- No Town Portal
- Walking Only
- No Potions (Wells Only)

**Themed:**
- Cosplay Run (thematic items only)
- SSF (Solo Self Found)

### Build Examples

**Amazon:**
- Javaazon (Lightning Fury)
- Bowazon (Strafe/Multiple Shot)
- Frost Maiden (Freezing Arrow)

**Necromancer:**
- Summonmancer (Skeleton Army)
- Bonemancer (Bone Spear)
- Poison Nova

**Sorceress:**
- Blizzard
- Lightning
- MeteorOrb

*...and many more!*

---

## 🎯 How to Use

1. **Configure**: Set rerolls and challenge count
2. **Spin**: Let fate choose your class
3. **Spin Again**: Get your build
4. **Challenges**: Spin for each challenge (if configured)
5. **Start Run**: Save your run to track progress
6. **Play**: Good luck in Sanctuary!
7. **Update**: Mark as Completed or Failed when done

---

## 🌟 Contributing

Found a bug? Have a build suggestion? Want to add more challenges?

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Blizzard Entertainment** for creating Diablo 2
- **react-custom-roulette** for the wheel component
- **Next.js team** for the amazing framework
- **The D2R community** for build inspiration

---

## 🔗 Links

- **Live Site**: [gheedsgamble.com](https://gheedsgamble.com)
- **GitHub**: [github.com/santboii/gheedsgamble](https://github.com/santboii/gheedsgamble)
- **Report Issues**: [GitHub Issues](https://github.com/santboii/gheedsgamble/issues)

---

<div align="center">

**Stay awhile and listen... to the wheel of fate!** 🎲🔥

Made with 💀 for the hardcore D2R community

</div>
