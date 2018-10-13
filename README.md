# Scrapy-IT_home_hot_comment


---

# 简介
Scrapy爬取IT之家热门评论

# 功能
爬取[IT之家首页][1]最热排行中的24小时阅读榜中的文章的热门评论，将文章标题、评论人、评论时间、评论内容、支持数和反对数保存在文本中或者mysql数据库中

# 效果图

# 注意事项

 1. 注意时效性，当前（2018/10/13）评论接口（https://dyn.ithome.com/ithome/getajaxdata.aspx） 的post数据为newsID、hash、pid、type，使用时请先注意该接口post数据是否改变
 2. 使用Mysql数据库时，请将ip、username、password和db换成本地数据库配置，并请根据建表语句先建表。
 3. 仅供学习交流使用，爬取速度不要设置太快，减少服务器压力

# 参考资料
 
  [1]: https://www.ithome.com/