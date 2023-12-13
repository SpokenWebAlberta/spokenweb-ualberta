---
layout: default
permalink: /stories/story/
title: audio
description: 'intervview.'
---

<h2 class='page-title'>{{ page.title }}</h2>

<ul>
{% for temp in site.pages %}
    {% if temp.url contains "/exhibits/" %}
        <li><a href="{{ temp.url | relative_url }}">{{temp.title}}</a></li>
    {% endif %}
{% endfor %}
</ul>

<audio controls>
  <source src="https://cbcradiolive.akamaized.net/hls/live/2041031/ES_R1EQQ/master.m3u8" >
  Your browser does not support the audio element.
</audio>
