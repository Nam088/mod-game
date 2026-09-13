using System;
using System.IO;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.UnrealTypes;

namespace WhiskerwoodConverter
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Whiskerwood Asset Inspector");
            string rootDir = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));
            string locEnPath = Path.Combine(rootDir, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset");

            try
            {
                var asset = new UAsset(locEnPath, EngineVersion.VER_UE5_5);
                Console.WriteLine($"[SUCCESS] Loaded with VER_UE5_5! Exports: {asset.Exports.Count}");
                for (int i = 0; i < asset.Exports.Count; i++)
                {
                    var exp = asset.Exports[i];
                    Console.WriteLine($"Export [{i}]: ObjectName={exp.ObjectName}, Type={exp.GetType().Name}");
                    if (exp is RawExport re)
                    {
                        Console.WriteLine($"  RawExport size: {re.Data.Length} bytes");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[FAIL] VER_UE5_5: {ex.ToString()}");
            }
        }
    }
}
