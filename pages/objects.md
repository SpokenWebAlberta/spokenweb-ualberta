---
layout: default
permalink: /audio/
title: All Objects
---

<h2 class='page-title'>All Audio</h2>

{% assign exhibits = site.pages | where: 'layout','object' %}
<ul>
  {% for exhibit in exhibits %}
    <li>
      <a href='{{ exhibit.url | absolute_url }}'>
        {{ site.data.objects[exhibit.iden].title }}
      </a>
    </li>
  {% endfor %}
</ul>
