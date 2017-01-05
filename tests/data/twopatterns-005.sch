<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-003.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern>
    <sch:title>Rule 1</sch:title>
    <sch:rule context="/">
      <sch:assert test="d:article">
        Expected an article
      </sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>Rule 2</sch:title>
    <sch:rule context="/d:article">
      <sch:assert test="d:section/@xml:id">
        Expected an xml:id on the first section
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
