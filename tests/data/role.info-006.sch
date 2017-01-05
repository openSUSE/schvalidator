<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-003.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern>
    <sch:title>Rule</sch:title>
    <sch:rule context="/d:article" role="error">
      <sch:assert test="d:abstract" role="info">
        Would be nice to have an abstract.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
