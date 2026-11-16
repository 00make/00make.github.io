# frozen_string_literal: true

# jekyll-link-attributes 用 Nokogiri/libxml2 重新序列化页面，libxml2 会自动补一个
# <meta http-equiv="Content-Type">，与模板里的 <meta charset> 重复。
# 在整站写盘后统一剥掉（仅当文件已有真正的 charset 声明时）。
Jekyll::Hooks.register :site, :post_write do |site|
  Dir.glob(File.join(site.dest, "**", "*.html")).each do |path|
    html = File.read(path)
    next unless html.match?(/<meta\s+charset\s*=/i)

    cleaned = html.gsub(%r{<meta\s+http-equiv=["']?Content-Type["']?\s+content=["']?text/html;\s*charset=UTF-8["']?\s*/?>}i, "")
    File.write(path, cleaned) if cleaned != html
  end
end