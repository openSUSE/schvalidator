<?xml version="1.0" encoding="UTF-8"?>
<!--

-->
<sch:schema id="schematron-001.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/>

  <sch:pattern id="all.general">
    <sch:title>General Rules</sch:title>
    <sch:rule context="/*">
      <sch:let name="root.version" value="@version"/>
      <sch:assert test="$root.version = '5.0'" >
        The @version attribute in the root element <sch:value-of
          select="local-name(.)"/> cannot have a value of <sch:value-of
            select="$root.version"/>.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
