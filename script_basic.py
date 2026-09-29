import pandas as pd
import re
import os

# ---------------- FILE PATH ----------------
file_path = r"C:\QA Files\aug\14-08-2026\Flipkart_SOV_2026-08-14.xlsx"
# ---------------- READ FILE (CSV / EXCEL AUTO) ----------------
ext = os.path.splitext(file_path)[1].lower()

if ext == ".csv":   
    df = pd.read_csv(file_path, keep_default_na=False)
elif ext in [".xlsx", ".xls"]:
    df = pd.read_excel(file_path, keep_default_na=False)
else:
    raise ValueError("❌ Unsupported file format. Please provide CSV or Excel file.")

print(f"\n✅ File loaded successfully: {file_path}")

# ---------------- SHOW COLUMNS ----------------
print("\nAvailable columns:")
for col in df.columns:
    print(col)

# ---------------- DUPLICATE CHECK ----------------
columns_input = input("\nEnter column names to check for duplicates (comma-separated): ")
columns_to_check = [col.strip() for col in columns_input.split(",")]

for col in columns_to_check:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' does not exist.")

duplicate_mask = df.duplicated(subset=columns_to_check, keep=False)
duplicates = df[duplicate_mask]

if not duplicates.empty:
    print(f"\n🔁 DUPLICATE ROWS FOUND BASED ON {columns_to_check}")
    print("-" * 60)
    for r in duplicates.index:
        print(f"Row {r + 1}: {df.loc[r, columns_to_check].to_dict()}")
else:
    print(f"\n✅ No duplicates found based on {columns_to_check}")

# ---------------- TEXT COLUMN SELECTION ----------------
text_cols = df.select_dtypes(include="object").columns

# ---------------- JUNK CHARACTERS ----------------
junk_chars = [

    # ==== HTML ENTITIES ====
    "&amp", "&lt", "&gt", "&nbsp", "&quot", "&apos", "&cent", "&pound",
    "&yen", "&euro", "&sect", "&copy", "&reg", "&trade", "&deg", "&plusmn",
    "&times", "&divide", "&ndash", "&mdash", "&lsquo", "&rsquo", "&ldquo",
    "&rdquo", "&bull", "&hellip", "&sup1", "&sup2", "&sup3", "&frac12",
    "&shy", "&#34", "&#39", "&#160", "&#8203", "&#8239", "&#xA0",
    "&hellip;", "&rsquor;", "&lsquor;", "&ensp;", "&emsp;", "&thinsp;",
    "&zwnj;", "&zwj;", "&lrm;", "&rlm;", "&sbquo;", "&bdquo;", "&permil;",
    "&oline;", "&frasl;", "&spades;", "&clubs;", "&hearts;", "&diams;",
    "&laquo;", "&raquo;", "&iexcl;", "&iquest;", "&para;", "&brvbar;",
    "&dagger;", "&rsquo;",

    # ==== HTML / XML TAGS ====
    "<br", "<p", "<div", "<span", "<style", "<footer", "<header", "<iframe",
    "<script", "<link", "<meta", "<input", "<body", "<html", "<table", "<tr",
    "<td", "<ul", "<li", "<strong", "<em", "<a ", "<img", "<h1", "<h2",
    "<h3", "<h4", "<h5", "<h6", "<form", "<nav", "<section", "<article",
    "</", "/>", "<!DOCTYPE", "<!--",

    # ==== ASCII CONTROL CHARACTERS ====
    "\t", "\n", "\r", "\f", "\b", "\v",

    # ==== OTHER SYMBOLS & NOISE ====
    "###","///", "\\\\", "||", "===","░", "▒", "▓", "▀", "▄", "█", "▌", "▐",

]

def find_junk(text):
    return [j for j in junk_chars if j in str(text)]

def count_extra_spaces(text):
    text = str(text)
    return (
        len(text) - len(text.lstrip()) +
        len(text) - len(text.rstrip()) +
        sum(len(m.group()) - 1 for m in re.finditer(r' {2,}', text))
    )

'''# ---------------- BLANK VALUE CHECK ----------------
print("\n❌ BLANK VALUES FOUND")
print("-" * 40)

for col in text_cols:
    blank_mask = df[col].astype(str).str.strip() == ""
    for r in df.index[blank_mask]:
        print(f"Row {r + 1}: {col} is blank")'''

# ---------------- JUNK & EXTRA SPACE CHECK ----------------
print("\n⚠️ JUNK CHARACTERS FOUND")
print("-" * 40)

for col in text_cols:
    for r in df.index:
        val = df.at[r, col]
        junk = find_junk(val)

        if junk:
            print(f"Row {r + 1}: {col} | junk -> {junk}")
