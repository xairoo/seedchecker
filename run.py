from bip_utils import (
    Bip39MnemonicValidator, Bip39Languages, Bip39SeedGenerator,
    Bip44, Bip44Coins, Bip44Changes
)

HIDE_INVALID = True

SEED_FILE = "seeds.txt"

SUPPORTED_CHAINS = {
    "eth": {
        "name": "Ethereum / BNB Smart Chain",
        "coin": Bip44Coins.ETHEREUM,
        "prefix": "0x"
    },
    "bnb": {
        "name": "BNB (Binance Chain, native)",
        "coin": Bip44Coins.BINANCE_CHAIN,
        "prefix": "bnb"
    },
    "btc": {
        "name": "Bitcoin (Legacy)",
        "coin": Bip44Coins.BITCOIN,
        "prefix": "1"
    },
    "ltc": {
        "name": "Litecoin",
        "coin": Bip44Coins.LITECOIN,
        "prefix": "L"
    }
}

def is_valid_seed(seed_phrase: str) -> bool:
    try:
        Bip39MnemonicValidator(Bip39Languages.ENGLISH).Validate(seed_phrase)
        return True
    except Exception as e:
        return False

def get_address_from_seed(seed_phrase: str, coin_type) -> str:
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
    bip44_ctx = Bip44.FromSeed(seed_bytes, coin_type)
    return bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

def main():
    print("=== Blockchain Selector ===")
    for key, info in SUPPORTED_CHAINS.items():
        print(f"{key} → {info['name']}")

    choice = input("Which blockchain do you want to use? (eth, bnb, btc, ltc): ").strip().lower()

    if choice not in SUPPORTED_CHAINS:
        print("❌ Unsupported chain.")
        return

    coin_info = SUPPORTED_CHAINS[choice]

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seeds = [line.strip() for line in f if line.strip()]

    print(f"\n🌐 Using derivation path for: {coin_info['name']}")
    print("-" * 40)
    print("Checking seedphrase...")

    for i, seed in enumerate(seeds):
        if not is_valid_seed(seed):
            if not HIDE_INVALID:
                print(f"[{i+1}/{len(seeds)}] ❌ Invalid seed.")
            continue

        try:
            address = get_address_from_seed(seed, coin_info["coin"])
            print(f"[{i+1}/{len(seeds)}] ✅ Address: {address}")

        except Exception as e:
            print(f"[{i+1}/{len(seeds)}] ⚠️ Error deriving address: {e}")

if __name__ == "__main__":
    main()
