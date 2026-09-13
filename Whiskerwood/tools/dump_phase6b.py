import json

def main():
    with open('translations/06_Quests_Events_Story.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    phase6b = data[335:671]
    print(f'Total items in Phase 6B: {len(phase6b)}')
    print(f'Start index 335: ID {phase6b[0]["id"]}, Key: {phase6b[0]["key"]}')
    print(f'End index 670: ID {phase6b[-1]["id"]}, Key: {phase6b[-1]["key"]}')

    with open('tools/phase6b_dump.txt', 'w', encoding='utf-8') as out:
        for i, item in enumerate(phase6b):
            out.write(f'[{i}] ID: {item["id"]} | Key: {item["key"]}\nEN: {item["source_en"]}\nVI: {item["target_vi"]}\n\n')

if __name__ == '__main__':
    main()
