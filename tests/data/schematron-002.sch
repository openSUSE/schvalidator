<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-001.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern>
    <sch:title>Rules</sch:title>
    <sch:rule context="/*">
      <sch:assert test="@version and @xml:id">
        Root element should have version and xml:id attributes!
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
