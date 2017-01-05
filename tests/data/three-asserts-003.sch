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
      <sch:assert test="count(d:para) = 2">
        I couldn't find two paras
      </sch:assert>
      <sch:assert test="d:para[1] = 'First'">
        The first para doesn't have 'First' as content.
      </sch:assert>
      <sch:assert test="d:para[2] = 'Second'">
        The first para doesn't have 'Second' as content.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
