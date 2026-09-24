# Which agent receives a request to start work?

The user should be able to ask Main, the product's PDO, or its PO. The receiving agent should preserve the requested scope and route it to the responsible delivery owner. A request to file work for later and a request to start delivery are different actions; choosing an addressee should not silently change either.

This describes the intended product behavior, not a newly published instruction. The follow-up question did not authorize new guidance.

## Current published guidance

- Main/default is explicitly called the user's front door. Its role explains setup and kungfu discovery, but does not clearly state that incoming product-delivery requests must reach the existing PDO.
- PDO core explicitly requires consultation with the addressed PO for every incoming delivery work item, before staffing. The PO decides the plan; PDO executes it and cannot amend it.
- PO core says to propose ready work to the delivery orchestrator, return topology decisions to the PDO, open no delivery assignments and parent no workers. This defines responsibility but does not fully spell out how an incoming direct user request becomes adopted PDO delivery custody.
- Shared manual defines work items, assignments and wakes. It does not provide a complete common intake contract for these three entry points.
- Live default-archetype is orchestrator. The learned agentic-engineering manifest and capability description still name product-owner as root. Neither fact alone implements the new PDO intake path. Bare-spawn default, bundle root and a product's existing delivery owner are separate choices.

Sources inspected on Gibson: identity/archetypes/default.toml; guidance/operating-manual.md; guidance/pdo.md; guidance/product-owner.md; kungfu/agentic-engineering/manifest.toml and capabilities.md; and the live config get default-archetype result. Main's stored served identity is e558f881, older than current published 312a6e17. Published-file inspection does not prove Main has received current wording.

## What is established

The completed Sol-low eval establishes one PDO-entry example: consult PO, obtain topology, staff a worker, recover record errors and close delivery. It also exposed a content-quality failure and extra coordination traffic. It does not establish entry-point equivalence.

The remaining product gap is to make and test a common outcome: a request through any supported entry point reaches the right existing PDO with complete context and one accountable work item; the PO supplies scope/topology judgment; the PDO staffs and carries delivery. Test direct Main, PDO and PO entry separately, including file-only requests and requests to begin work. No such additional eval, guidance edit or routing configuration change was performed by this investigation.
