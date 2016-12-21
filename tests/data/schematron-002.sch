<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-001.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern id="all.general">
    <sch:title>General Rules</sch:title>
    <sch:rule context="/d:article">
      <sch:assert test="d:warning/d:title">
        The warning element has no title!
      </sch:assert>
    </sch:rule>
    <sch:rule context="/d:article">
      <sch:report test="not(d:warning/d:warning)">
        There shouldn't be a warning inside another warning
      </sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
