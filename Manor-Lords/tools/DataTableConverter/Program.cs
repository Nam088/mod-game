using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.UnrealTypes;

namespace DataTableConverter
{
    class Program
    {
        static void Main(string[] args)
        {
            string hoodDir = @"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse";
            string transDir = @"d:\mod-game\Manor-Lords\translations";
            string buildDir = @"d:\mod-game\Manor-Lords\build\ManorLords\Content\Translation\HoodedHorse";
            Directory.CreateDirectory(buildDir);

            var jsonFiles = Directory.GetFiles(transDir, "DT_Translation_*.json");
            Console.WriteLine($"Found {jsonFiles.Length} translation JSON files. Starting build to {buildDir}...\n");

            int totalPatchedFiles = 0;
            int totalPatchedStrings = 0;

            foreach (var jsonPath in jsonFiles)
            {
                string tableName = Path.GetFileNameWithoutExtension(jsonPath);
                string uassetPath = Path.Combine(hoodDir, $"{tableName}.uasset");

                if (!File.Exists(uassetPath))
                {
                    Console.WriteLine($"[WARN] Source asset not found: {uassetPath}");
                    continue;
                }

                string jsonContent = File.ReadAllText(jsonPath, Encoding.UTF8);
                var entries = JsonConvert.DeserializeObject<List<TranslationEntry>>(jsonContent);
                if (entries == null || entries.Count == 0) continue;

                var asset = new UAsset(uassetPath, EngineVersion.VER_UE5_5);
                if (asset.Exports.Count == 0 || !(asset.Exports[0] is RawExport rawExport))
                {
                    Console.WriteLine($"[WARN] No RawExport found in {tableName}");
                    continue;
                }

                byte[] data = rawExport.Data;

                // Sort entries in descending order of Offset to maintain valid offsets during length changes
                var sortedEntries = entries.OrderByDescending(e => e.Offset).ToList();
                int patchedInFile = 0;

                foreach (var entry in sortedEntries)
                {
                    if (entry.Offset < 0 || entry.Offset >= data.Length) continue;

                    string viText = string.IsNullOrEmpty(entry.Target_VI) ? entry.Source_EN : entry.Target_VI;

                    int origLen = BitConverter.ToInt32(data, entry.Offset);
                    int origTotalLen = 0;
                    if (origLen > 0)
                    {
                        origTotalLen = 4 + origLen;
                    }
                    else if (origLen < 0)
                    {
                        origTotalLen = 4 + ((-origLen) * 2);
                    }
                    else
                    {
                        origTotalLen = 4;
                    }

                    if (entry.Offset + origTotalLen > data.Length) continue;

                    bool isUnicode = viText.Any(c => c > 127);
                    byte[] newChunk;

                    if (isUnicode)
                    {
                        int charCount = viText.Length + 1;
                        int newLen = -charCount; // Negative length indicates UTF-16 LE in Unreal Engine FString!
                        byte[] textBytes = Encoding.Unicode.GetBytes(viText);

                        newChunk = new byte[4 + (charCount * 2)];
                        BitConverter.GetBytes(newLen).CopyTo(newChunk, 0);
                        textBytes.CopyTo(newChunk, 4);
                        newChunk[newChunk.Length - 2] = 0;
                        newChunk[newChunk.Length - 1] = 0;
                    }
                    else
                    {
                        int charCount = viText.Length + 1;
                        int newLen = charCount; // Positive length indicates ASCII/ANSI in Unreal Engine FString
                        byte[] textBytes = Encoding.ASCII.GetBytes(viText);

                        newChunk = new byte[4 + charCount];
                        BitConverter.GetBytes(newLen).CopyTo(newChunk, 0);
                        textBytes.CopyTo(newChunk, 4);
                        newChunk[newChunk.Length - 1] = 0;
                    }

                    // Resize byte array and splice
                    byte[] newData = new byte[data.Length - origTotalLen + newChunk.Length];
                    Buffer.BlockCopy(data, 0, newData, 0, entry.Offset);
                    Buffer.BlockCopy(newChunk, 0, newData, entry.Offset, newChunk.Length);
                    Buffer.BlockCopy(data, entry.Offset + origTotalLen, newData, entry.Offset + newChunk.Length, data.Length - (entry.Offset + origTotalLen));

                    data = newData;
                    patchedInFile++;
                }

                rawExport.Data = data;

                string outUasset = Path.Combine(buildDir, $"{tableName}.uasset");
                asset.Write(outUasset);

                totalPatchedFiles++;
                totalPatchedStrings += patchedInFile;
                Console.WriteLine($"  [OK] {tableName,-38} : {patchedInFile,5} strings patched -> ({data.Length:N0} bytes)");
            }

            Console.WriteLine("\n=======================================================");
            Console.WriteLine($"BUILD COMPLETE: {totalPatchedFiles} DataTables ({totalPatchedStrings} strings) successfully compiled to UE5.5 binary format!");
            Console.WriteLine($"Output: {buildDir}");
        }
    }

    class TranslationEntry
    {
        [JsonProperty("key")]
        public string Key { get; set; } = "";

        [JsonProperty("en")]
        public string Source_EN { get; set; } = "";

        [JsonProperty("vi")]
        public string Target_VI { get; set; } = "";

        [JsonProperty("offset")]
        public int Offset { get; set; }

        [JsonProperty("length")]
        public int Length { get; set; }
    }
}

