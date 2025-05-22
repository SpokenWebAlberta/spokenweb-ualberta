---
layout: page
permalink: /exhibits/
title: All Exhibits
description: 'Archive of exhibits.'
---

<h2 class='page-title'>{{ page.title }}</h2>

<ul>
{% for temp in site.pages %}
    {% if temp.url contains "/exhibits/" %}
        <li><a href="{{ temp.url | relative_url }}">{{temp.title}}</a></li>
    {% endif %}
{% endfor %}
</ul>