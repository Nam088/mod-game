using UnityEngine;
using Newtonsoft.Json;
using System.IO;
using System.Collections.Generic;
using System;

namespace VietnameseTranslation
{
    public class WorldBoxMod : MonoBehaviour
    {
        private static bool _initialized = false;

        void Awake()
        {
            Debug.Log("[VietnameseTranslation] Mod Awake called!");
        }

        void Start()
        {
            Debug.Log("[VietnameseTranslation] Mod Start called!");
        }

        void Update()
        {
            if (_initialized) return;

            // Wait until the game is fully loaded
            if (Config.game_loaded)
            {
                _initialized = true;
                LoadTranslation();
            }
        }

        void LoadTranslation()
        {
            try
            {
                List<string> candidatePaths = new List<string>();

                // 1. Current mod DLL directory
                string currentModDir = Path.GetDirectoryName(typeof(WorldBoxMod).Assembly.Location);
                if (!string.IsNullOrEmpty(currentModDir))
                {
                    candidatePaths.Add(Path.Combine(currentModDir, "vi.json"));
                    candidatePaths.Add(Path.Combine(currentModDir, "..", "vi.json"));
                }

                // 2. Local StreamingAssets/mods/vi.json and subfolders
                string streamingMods = Path.Combine(Application.streamingAssetsPath, "mods");
                candidatePaths.Add(Path.Combine(streamingMods, "vi.json"));
                candidatePaths.Add(Path.Combine(streamingMods, "VietnameseTranslation", "vi.json"));

                // 3. Root game Mods/VietnameseTranslation/vi.json
                string rootMods = Path.Combine(Application.dataPath, "..", "Mods");
                candidatePaths.Add(Path.Combine(rootMods, "vi.json"));
                candidatePaths.Add(Path.Combine(rootMods, "VietnameseTranslation", "vi.json"));

                string targetPath = null;
                foreach (var path in candidatePaths)
                {
                    if (!string.IsNullOrEmpty(path) && File.Exists(path))
                    {
                        targetPath = Path.GetFullPath(path);
                        break;
                    }
                }

                if (targetPath != null)
                {
                    Debug.Log($"[VietnameseTranslation] Loading translation from: {targetPath}");
                    string json = File.ReadAllText(targetPath);
                    var dict = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);
                    
                    int count = 0;
                    if (dict != null)
                    {
                        foreach (var kvp in dict)
                        {
                            LocalizedTextManager.add(kvp.Key, kvp.Value, true, "VietnameseTranslation", false);
                            count++;
                        }
                    }
                    
                    LocalizedTextManager.updateTexts();
                    Debug.Log($"[VietnameseTranslation] Successfully loaded and updated {count} Vietnamese translation strings!");
                }
                else
                {
                    Debug.LogError($"[VietnameseTranslation] Could not find vi.json in any candidate path!");
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[VietnameseTranslation] Error loading translation: {ex.Message}");
                Debug.LogError(ex.StackTrace);
            }
        }
    }
}
