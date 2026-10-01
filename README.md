# mkbody

日常的に食べる食品の栄養素をCSVで管理するリポジトリ。

## 構成

```
nutrition.csv          栄養素データ（1行 = 1食品）
rawdata/               食品ラベルの写真（JPG）
recipes/               自炊メニューのレシピ集（栄養メモ付き）
scripts/strip_exif.py  JPGからEXIF等のメタデータを除去するスクリプト
```

## nutrition.csv

食品ごとに栄養成分表示の値を記録する。

- 基準量はなるべく「1食分」に揃える。市販品はラベルの表示単位（1袋、1パック等）をそのまま使う
- 自炊の作り置き（低温調理鶏胸肉、プルドポーク等）は100gを1食分として換算する
- 値の出典はラベルの栄養成分表示を優先する。ラベルがないものは日本食品標準成分表（八訂）ベースの推定値
- ラベルが「0.48~0.66」のような幅表記の場合は範囲のまま記録する
- 新しい栄養素が出てきたら列を末尾に追加する

## 画像追加のワークフロー

1. ラベル写真（HEIC）を `rawdata/` に入れる
2. 英語ファイル名でJPGに変換する

   ```sh
   sips -s format jpeg <name>.heic --out <english-name>.jpg
   ```

3. EXIF等のメタデータを除去する（撮影日時・機材情報・GPSを公開しないため）

   ```sh
   python3 scripts/strip_exif.py rawdata/*.jpg
   ```

4. 元のHEICを削除する
5. ラベルを読み取って `nutrition.csv` に行を追加する

## License

[MIT](LICENSE)
