export function useNickname() {
    let nickname = localStorage.getItem('nickname')
    if (!nickname) {
        return generateNickname()
    }
    return nickname
}

export function useSetNickname(nickname: string) {
    localStorage.setItem('nickname', nickname)
}

const ADJECTIVES = [
    // gamer
    'Rapid',
    'Frost',
    'Steel',
    'Shadow',
    'Hyper',
    'Ghost',
    'Neon',
    'Blitz',
    'Swift',
    'Iron',
    'Void',
    'Storm',
    'Sonic',
    'Rogue',
    'Apex',
    // cool
    'Silent',
    'Slick',
    'Zero',
    'Prime',
    'Sharp',
    'Bold',
    'Hex',
    // dark
    'Cursed',
    'Hollow',
    'Grim',
    'Ashen',
    'Crimson',
    'Pale',
    'Dread',
    'Sable',
    'Thorn',
    'Wretched',
    // sci-fi
    'Quantum',
    'Nano',
    'Cyber',
    'Neural',
    'Orbital',
    'Plasma',
    'Binary',
    'Mech',
    'Astro',
    'Xeno',
    // fantasy
    'Ancient',
    'Arcane',
    'Mythic',
    'Sacred',
    'Runic',
    'Primal',
    'Astral',
    'Ember',
    'Twilight',
    'Elven',
]

const NOUNS = [
    // gamer
    'Slayer',
    'Sniper',
    'Blade',
    'Reaper',
    'Hunter',
    'Crusher',
    'Phantom',
    'Ace',
    'Wolf',
    'Hawk',
    'Viper',
    'Titan',
    'Wraith',
    'Surge',
    'Frag',
    // cool
    'Wave',
    'Drift',
    'Flux',
    'Edge',
    'Node',
    'Veil',
    'Trace',
    'Arc',
    // dark
    'Specter',
    'Omen',
    'Dirge',
    'Shroud',
    'Abyss',
    'Blight',
    'Wraith',
    'Bane',
    'Shade',
    'Malice',
    // sci-fi
    'Nexus',
    'Core',
    'Matrix',
    'Pulse',
    'Array',
    'Beacon',
    'Reactor',
    'Circuit',
    'Synapse',
    'Vector',
    // fantasy
    'Drake',
    'Sage',
    'Forge',
    'Keeper',
    'Pyre',
    'Shard',
    'Rune',
    'Sigil',
    'Fable',
    'Grove',
]

export function generateNickname(): string {
    const adj = ADJECTIVES[Math.floor(Math.random() * ADJECTIVES.length)] ?? ''
    const noun = NOUNS[Math.floor(Math.random() * NOUNS.length)] ?? ''
    const num = String(Math.floor(Math.random() * 900) + 100)
    return adj + noun + num
}
