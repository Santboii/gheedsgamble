export type ClassName = "Amazon" | "Assassin" | "Necromancer" | "Barbarian" | "Paladin" | "Sorceress" | "Druid";

export interface Build {
    name: string;
    description: string;
}

export interface Challenge {
    id: string;
    text: string;
    description: string;
    weight: number; // Higher weight = higher chance
}

export const CLASSES: ClassName[] = [
    "Amazon", "Assassin", "Necromancer", "Barbarian", "Paladin", "Sorceress", "Druid"
];

export const BUILDS: Record<ClassName, Build[]> = {
    Amazon: [
        { name: "Javaazon", description: "Max: Lightning Fury, Charged Strike, Lightning Bolt, Power Strike" },
        { name: "Bowazon (Physical)", description: "Max: Strafe, Multiple Shot, Guided Arrow, Valkyrie" },
        { name: "Frost Maiden", description: "Max: Freezing Arrow, Cold Arrow, Valkyrie" },
        { name: "Fendazon", description: "Max: Fend, Jab, Critical Strike, Penetrate" },
        { name: "Poison Java", description: "Max: Poison Javelin, Plague Javelin, Valkyrie" },
        { name: "Magezon", description: "Max: Freezing Arrow, Exploding Arrow, Fire Arrow, Cold Arrow" },
        { name: "Hybrid Bow/Java", description: "Max: Lightning Fury, Guided Arrow, Valkyrie" },
        { name: "Immolation Amazon", description: "Max: Immolation Arrow, Exploding Arrow, Fire Arrow" }
    ],
    Assassin: [
        { name: "Trapsin (Lightning)", description: "Max: Lightning Sentry, Death Sentry, Charged Bolt Sentry, Shock Web" },
        { name: "Kicksin", description: "Max: Dragon Talon, Venom, Death Sentry" },
        { name: "Mosaic Sin", description: "Max: Phoenix Strike, Claws of Thunder, Blades of Ice" },
        { name: "Blade Fury", description: "Max: Blade Fury, Blade Sentinel, Venom" },
        { name: "Riftpsin", description: "Max: Dragon Talon, Venom, Death Sentry, Lightning Sentry" },
        { name: "Fire Trapsin", description: "Max: Wake of Fire, Wake of Inferno, Fire Blast" }
    ],
    Necromancer: [
        { name: "Summonmancer", description: "Max: Raise Skeleton, Skeleton Mastery, Corpse Explosion" },
        { name: "Bonemancer", description: "Max: Bone Spear, Bone Spirit, Bone Wall, Bone Prison" },
        { name: "Poison Nova", description: "Max: Poison Nova, Poison Explosion, Poison Dagger" },
        { name: "Daggermancer", description: "Max: Poison Dagger, Poison Nova, Poison Explosion" },
        { name: "Explosionmancer", description: "Max: Corpse Explosion, Bone Wall (synergy), Bone Prison" },
        { name: "Golemancer", description: "Max: Golem Mastery, Iron Golem, Blood Golem, Clay Golem" }
    ],
    Barbarian: [
        { name: "Whirlwind", description: "Max: Whirlwind, Weapon Mastery, Battle Orders, Shout" },
        { name: "Frenzy", description: "Max: Frenzy, Double Swing, Taunt, Battle Orders" },
        { name: "Singer (Warcry)", description: "Max: War Cry, Battle Cry, Battle Orders, Howl" },
        { name: "Throw Barb", description: "Max: Double Throw, Throwing Mastery, Battle Orders" },
        { name: "Berserk", description: "Max: Berserk, Howl, Weapon Mastery, Battle Orders" },
        { name: "Wolf Barb", description: "Max: Weapon Mastery, Battle Orders, Iron Skin (Wolf skills from helm)" },
        { name: "Concentrate", description: "Max: Concentrate, Weapon Mastery, Battle Orders, Iron Skin" },
        { name: "Leap Attack", description: "Max: Leap Attack, Leap, Battle Orders, Weapon Mastery" }
    ],
    Paladin: [
        { name: "Hammerdin", description: "Max: Blessed Hammer, Concentration, Vigor, Blessed Aim" },
        { name: "Zealot", description: "Max: Zeal, Fanaticism, Sacrifice, Holy Shield" },
        { name: "Smiter", description: "Max: Smite, Holy Shield, Fanaticism, Defiance" },
        { name: "FoHdin", description: "Max: Fist of the Heavens, Holy Bolt, Holy Shock" },
        { name: "Auradin (Holy Fire)", description: "Max: Resist Fire, Salvation (Aura from gear)" },
        { name: "Dragondin", description: "Max: Resist Fire, Salvation (Holy Fire from gear)" }
    ],
    Sorceress: [
        { name: "Blizzard", description: "Max: Blizzard, Ice Blast, Glacial Spike, Cold Mastery" },
        { name: "Lightning", description: "Max: Lightning, Chain Lightning, Lightning Mastery, Charged Bolt" },
        { name: "MeteorOrb", description: "Max: Frozen Orb, Meteor, Fire Ball, Fire Mastery" },
        { name: "Fireball", description: "Max: Fire Ball, Meteor, Fire Bolt, Fire Mastery" },
        { name: "Enchantress", description: "Max: Enchant, Warmth, Fire Mastery" },
        { name: "Bear Sorc", description: "Max: Enchant, Warmth, Lightning Mastery (Dreams)" },
        { name: "Nova Sorc", description: "Max: Nova, Lightning Mastery, Charged Bolt, Static Field" },
        { name: "Hydra", description: "Max: Hydra, Fire Mastery, Fire Ball, Warmth" }
    ],
    Druid: [
        { name: "Wind Druid", description: "Max: Tornado, Hurricane, Cyclone Armor, Twister" },
        { name: "Fury Werewolf", description: "Max: Fury, Lycanthropy, Werewolf, Heart of Wolverine" },
        { name: "Fire Druid", description: "Max: Fissure, Volcano, Armageddon, Molten Boulder" },
        { name: "Summoner Druid", description: "Max: Summon Grizzly, Summon Dire Wolf, Heart of Wolverine" },
        { name: "Maul Werebear", description: "Max: Maul, Shockwave, Lycanthropy, Werebear" },
        { name: "Rabies", description: "Max: Rabies, Poison Creeper, Lycanthropy" }
    ]
};

export const CHALLENGES: Challenge[] = [
    { id: "c1", text: "No Runewords", description: "Cannot create or use runewords", weight: 50 },
    { id: "c2", text: "No Teleport", description: "Teleport skill and Enigma are forbidden", weight: 80 },
    { id: "c3", text: "SSF (Solo Self Found)", description: "No trading, no help from other players", weight: 90 },
    { id: "c4", text: "No Mercenary", description: "Must adventure alone without a hireling", weight: 60 },
    { id: "c5", text: "Walking Only (No Run)", description: "Toggle run off, walk everywhere", weight: 40 },
    { id: "c6", text: "Rare Items Only", description: "Can only equip rare (yellow) items", weight: 30 },
    { id: "c7", text: "Magic Items Only (Blue)", description: "Can only equip magic (blue) items", weight: 20 },
    { id: "c8", text: "No Potions (Wells Only)", description: "Cannot use potions, only healing wells", weight: 10 },
    { id: "c9", text: "Pacifist (Thorns/Auras)", description: "Cannot directly attack, only reflect/aura damage", weight: 5 },
    { id: "c11", text: "No Rare Items", description: "Cannot equip rare (yellow) items", weight: 40 },
    { id: "c12", text: "No Unique Items", description: "Cannot equip unique (gold) items", weight: 30 },
    { id: "c13", text: "No Set Items", description: "Cannot equip set (green) items", weight: 60 },
    { id: "c14", text: "Cosplay Run", description: "Must use items matching a specific theme", weight: 35 },
    { id: "c15", text: "Glass Cannon", description: "No defensive stats allowed (life, resists, defense)", weight: 15 },
    { id: "c16", text: "No Synergies", description: "Cannot invest in skills that synergize with main skill", weight: 45 },
    { id: "c17", text: "No Waypoints", description: "Must walk everywhere (town portals allowed)", weight: 25 },
    { id: "c18", text: "No Town Portal", description: "Can only use waypoints to travel", weight: 35 },
    { id: "c19", text: "No Charms", description: "Inventory only for items, no charms allowed", weight: 55 },
    { id: "c20", text: "No Crafting", description: "Cannot use Horadric Cube for crafting", weight: 50 },
    { id: "c21", text: "First Skill Tree Banned", description: "Cannot use any skills from the first skill tree", weight: 45 },
    { id: "c22", text: "Second Skill Tree Banned", description: "Cannot use any skills from the second skill tree", weight: 45 },
    { id: "c23", text: "Third Skill Tree Banned", description: "Cannot use any skills from the third skill tree", weight: 45 },
    { id: "c24", text: "Drop on Level", description: "Must drop one equipped item every time you level up", weight: 25 },
    { id: "c25", text: "No Repairing Gear", description: "Cannot repair equipment, must replace when broken", weight: 35 },
    { id: "c26", text: "No Trading with Vendors", description: "Cannot buy or sell items to NPCs", weight: 40 },
    { id: "c27", text: "No Rejuvenation Potions", description: "Cannot use rejuvenation potions", weight: 60 },
    { id: "c28", text: "No Mana Potions", description: "Cannot use mana potions, natural regen only", weight: 50 },
    { id: "c29", text: "Same Song on Repeat", description: "Must listen to the same song on loop while playing", weight: 8 },
    { id: "c30", text: "Ethereals Only", description: "Can only equip ethereal items (cannot be repaired)", weight: 20 },
    { id: "c31", text: "No Shields", description: "Cannot equip shields or off-hand items", weight: 55 },
    { id: "c32", text: "Bow Only", description: "Can only use bows as weapons (no melee, no crossbows)", weight: 30 },
    { id: "c33", text: "Shirtless Wonder", description: "Cannot equip chest armor (embrace the breeze)", weight: 40 },
];

