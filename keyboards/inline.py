from .builder import Mode, simple_keyboard_builder

kb_choose_game = simple_keyboard_builder(
    [
        [
            ['🎲 Куб', 'cube'],
            ['🎯 Дартс', 'darts'],
            ['🏀 Баскетбол', 'basketball']
        ],
        [
            ['⚽ Футбол', 'football'],
            ['🎳 Боулинг', 'bouling'],
            ['🎰 Игровой автомат', 'slot_machine']
        ],
        [
            ['🔢 Числа', 'numbers'], ['🪙 Орел и решка', 'heads_and_tails']
        ]
    ],
    Mode.INLINE
)