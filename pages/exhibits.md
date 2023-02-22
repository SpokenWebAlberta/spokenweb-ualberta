---
layout: default
permalink: /exhibits/
title: Featured Exhibits
---

<h2 class='page-title'>Featured Exhibits</h2>

{% assign exhibits = site.exhibits | where: 'layout','exhibit' %}
<ul>
  {% for exhibit in exhibits %}
    <li>
      <a href='{{ exhibit.url | absolute_url }}'>
        {{ exhibit.title }}
      </a>
    </li>
  {% endfor %}
</ul>
