<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-003.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern>
    <sch:title>Rules</sch:title>
    <sch:rule context="/d:article">
      <sch:assert test="count(d:section) = 1">
        Expected one section after article
      </sch:assert>
      <sch:assert test="count(d:section/d:section) != 1">
        Lonely section
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
