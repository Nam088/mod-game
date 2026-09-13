import json

def main():
    with open('translations/06_Quests_Events_Story.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    phase6c = data[671:]
    print(f'Total items in Phase 6C: {len(phase6c)}')
    print(f'Start index 671: ID {phase6c[0]["id"]}, Key: {phase6c[0]["key"]}')
    print(f'End index {671 + len(phase6c) - 1}: ID {phase6c[-1]["id"]}, Key: {phase6c[-1]["key"]}')

    with open('tools/phase6c_dump.txt', 'w', encoding='utf-8') as out:
        for i, item in enumerate(phase6c):
            out.write(f'[{i}] ID: {item["id"]} | Key: {item["key"]}\nEN: {item["source_en"]}\nVI: {item["target_vi"]}\n\n')

if __name__ == '__main__':
    main()
