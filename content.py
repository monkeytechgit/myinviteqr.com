# Page copy and SEO metadata. Edit here, then run: python3 build.py
# Titles stay near 60 characters and descriptions near 155 so search results do not truncate them.

HOME_FAQ = [
    ("What is a digital invitation with a QR code?",
     "A digital invitation is an online invitation guests open on their phone. MyInviteQR gives every invitation its own link and QR code, so guests can scan the code or tap the link to see the details and RSVP in seconds."),
    ("How much does MyInviteQR cost?",
     "Designing your invitation is free. When you are ready to publish, Essential is $9.99 and Premium is $19.99, paid once per event. There is no subscription."),
    ("Do my guests need to download an app or create an account?",
     "No. Guests open your invitation in the web browser on their phone or computer and reply with one tap. No app and no account."),
    ("How do I send my digital invitation?",
     "Publish your event and share your link by text message, WhatsApp, email or social media, or print the QR code on cards, signs and posters. You can also send a personal link to each guest with Premium."),
    ("Can I track who opened my invitation and who replied?",
     "Yes. Your dashboard shows who replied yes, no or maybe, how many people are in each party and who opened the invitation but has not answered yet."),
    ("Can I customize the design?",
     "Absolutely. Start from one of 50 templates and change the text, fonts, colors and photos. You can drag, resize and rotate any element, and choose from more than 130 color palettes."),
    ("How many guests can I invite?",
     "Essential supports up to 50 guests. Premium supports up to 1,000 guests, so it works for everything from a small dinner to a large wedding."),
    ("How long does my invitation stay online?",
     "Each plan keeps your invitation active for 90 days after you publish. You can add a 6-month extension for $6.99 whenever you need more time."),
]

PAGES = {
    "home": dict(
        title="Digital Invitations with QR Code – Create Online | MyInviteQR",
        og_title="Digital Invitations with QR Code | MyInviteQR",
        desc="Create beautiful digital invitations with a QR code in minutes. Send one link, track RSVPs online and skip the printing. Design free, pay only to publish.",
        keywords="digital invitations, QR code invitations, online invitations, e-invitations, digital wedding invitations, birthday invitations online, baby shower invitations, quinceañera invitations, online RSVP, invitation maker, send invitations by text, paperless invitations, invitation templates, RSVP tracker, invitation with QR code",
    ),
    "how": dict(
        title="How to Create a Digital Invitation Online | MyInviteQR",
        desc="See how to make a digital invitation with a QR code in four easy steps: create your event, pick a template, customize it and share it with guests.",
        keywords="how to make a digital invitation, create online invitation, make invitation with QR code, how to send digital invitations, invitation maker online, e-invite maker",
    ),
    "pricing": dict(
        title="Pricing – Digital Invitations from $9.99 | MyInviteQR",
        desc="Simple one-time pricing for digital invitations with QR code and RSVP. Essential $9.99, Premium $19.99. No subscription. Design free, pay only to publish.",
        keywords="digital invitation pricing, online invitation cost, e-invitation price, QR code invitation price, invitation maker pricing, affordable digital invitations",
    ),
    "templates": dict(
        title="50 Digital Invitation Templates | MyInviteQR",
        desc="Browse 50 designer digital invitation templates for weddings, birthdays, baby showers, quinceañeras and corporate events. Customize every detail online.",
        keywords="digital invitation templates, wedding invitation templates, birthday invitation templates, baby shower invitation templates, quinceañera invitation templates, editable invitation templates, online invitation designs",
    ),
    "faq": dict(
        title="FAQ – Digital Invitations & QR Codes | MyInviteQR",
        desc="Answers to common questions about digital invitations, QR codes, online RSVP, guest limits, pricing and how MyInviteQR works for your event.",
        keywords="digital invitation faq, QR code invitation questions, online rsvp help, how do digital invitations work",
    ),
    "contact": dict(
        title="Contact MyInviteQR | Support for Digital Invitations",
        desc="Have a question about your digital invitation, order or event? Contact the MyInviteQR support team by email. We reply within one business day.",
        keywords="myinviteqr contact, invitation support, digital invitation help",
    ),
    "privacy": dict(title="Privacy Policy | MyInviteQR", desc="How MyInviteQR collects, uses and protects your information when you create digital invitations and manage RSVPs.",
                    keywords="myinviteqr privacy policy", h1="Privacy Policy", lead="How we handle your information.", robots="index, follow"),
    "terms": dict(title="Terms of Service | MyInviteQR", desc="The terms that apply when you use MyInviteQR to create digital invitations, share them and collect RSVPs.",
                  keywords="myinviteqr terms of service", h1="Terms of Service", lead="The rules for using MyInviteQR.", robots="index, follow"),
    "blog": dict(
        title="Invitation Ideas, Wording & Guides | MyInviteQR Blog",
        desc="Invitation wording ideas, etiquette tips and step-by-step guides for weddings, birthdays, baby showers and more from the MyInviteQR blog.",
        keywords="invitation wording, invitation ideas, digital invitation guides, wedding invitation wording, party planning tips"),
    "404": dict(title="Page Not Found | MyInviteQR", desc="This page could not be found. Explore MyInviteQR digital invitations and templates.", keywords="", robots="noindex, follow"),
    "wedding": dict(
        title="Digital Wedding Invitations Online | MyInviteQR",
        desc="Create elegant digital wedding invitations with a QR code and online RSVP. Share one link with every guest and track replies in real time.",
        keywords="digital wedding invitations, online wedding invitations, wedding invitations with QR code, wedding e-invites, electronic wedding invitations, wedding RSVP online, save the date digital, paperless wedding invitations"),
    "birthday": dict(
        title="Digital Birthday Invitations Online | MyInviteQR",
        desc="Make fun digital birthday invitations with a QR code in minutes. Kids and adult designs, online RSVP and one link to share by text or email.",
        keywords="digital birthday invitations, online birthday invitations, birthday invitations with QR code, kids birthday invitation online, birthday party e-invite, birthday RSVP online, electronic birthday invitations"),
    "baby": dict(
        title="Digital Baby Shower Invitations | MyInviteQR",
        desc="Create sweet digital baby shower invitations with a QR code and online RSVP. Share the details, collect replies and skip the paper.",
        keywords="digital baby shower invitations, online baby shower invitations, baby shower e-invite, baby shower invitation with QR code, baby shower RSVP online, gender reveal invitation online"),
    "quince": dict(
        title="Digital Quinceañera Invitations | MyInviteQR",
        desc="Design stunning digital quinceañera invitations with a QR code and online RSVP for up to 1,000 guests. Elegant templates in English and Spanish.",
        keywords="digital quinceañera invitations, quinceanera invitations online, quince invitations with QR code, sweet 15 invitations, quinceañera e-invite, invitaciones de quinceañera digitales, sweet 16 invitations online"),
    "corporate": dict(
        title="Corporate Event Invitations Online | MyInviteQR",
        desc="Send professional digital invitations for corporate events, galas and launches. QR check-in ready, online RSVP and guest tracking for up to 1,000 guests.",
        keywords="corporate event invitations, business event invitation online, company party invitations digital, conference invitation, gala invitation online, corporate RSVP, event invitation with QR code"),
    "qr": dict(
        title="QR Code Invitations – Create & Share Online | MyInviteQR",
        desc="Create QR code invitations guests scan to open your event details and RSVP. Add the code to printed cards, signs and screens. Ready in minutes.",
        keywords="QR code invitations, invitation with QR code, QR code wedding invitation, QR code party invitation, scan to RSVP, QR code invitation maker, QR invitation template, digital invitation QR"),
    "rsvp": dict(
        title="Online RSVP for Events – Track Guests | MyInviteQR",
        desc="Collect RSVPs online with a simple link or QR code. See who is coming, who opened your invitation and export your guest list. No app for guests.",
        keywords="online RSVP, RSVP tracker, RSVP online free alternative, event RSVP website, guest list manager, RSVP link, collect RSVPs online, wedding RSVP online, party RSVP"),
}

USE_CASES = {
    "wedding": dict(
        name="Wedding", crumb="Wedding invitations",
        h1="Digital wedding invitations your guests will love",
        lead="Share your day with one beautiful link. Add your ceremony details, collect RSVPs and update anything in seconds, all with a QR code that works on save-the-dates, programs and signs.",
        why_title="Why couples choose digital wedding invitations", why_sub="Elegant, affordable and far easier to manage than paper.",
        why=[("clock", "Send in minutes, not weeks", "No printing, no postage and no waiting on the mail. Share your invitation as soon as it is ready."),
             ("users", "RSVPs without the chase", "Guests answer from their phone with their party size. You see every reply in one list."),
             ("edit", "Fix details any time", "Venue changed? Timeline updated? Edit once and every guest sees the latest version.")],
        steps_title="Create your wedding invitation in four steps",
        tpl_title="Wedding invitation templates", tpl_sub="Romantic arches, timeless frames and modern editorial layouts.",
        templates=["Garden Romance", "Golden Arch", "Ceremony Frame", "Love Story"],
        wording_title="Wedding invitation wording ideas", wording_intro="Not sure what to write? Start with one of these and make it your own.",
        wording=["Together with their families, Emma Carter and Jack Morgan invite you to celebrate their wedding on Saturday, June 14, 2026 at 4:00 PM.",
                 "We are getting married! Join us for an evening of love, laughter and dancing. Kindly reply by May 1.",
                 "Two hearts, one love story. Please join us as we say &ldquo;I do.&rdquo;"],
        split_title="Save-the-dates, programs and signs with a QR code", split_text="Every invitation includes a QR code you can drop into printed pieces. Guests scan it at the venue to see the schedule, the map and the RSVP button.",
        split_checks=["Match your wedding colors with 130+ palettes", "Add engagement photos anywhere in the design", "Share a personal link with each guest (Premium)", "Up to 1,000 guests with Premium"],
        split_alt="Wedding invitation with a QR code on a printed save-the-date",
        faqs=[("When should I send digital wedding invitations?", "Send save-the-dates 6 to 9 months before the wedding and the full invitation 6 to 8 weeks before. Digital invitations let you send them whenever you are ready."),
              ("Can I use MyInviteQR for both the save-the-date and the invitation?", "Yes. Publish one invitation and update it as your plans firm up. The same link and QR code keep working, and guests always see the latest details."),
              ("How many wedding guests can I invite?", "Essential supports up to 50 guests. Premium supports up to 1,000, which covers almost any wedding."),
              ("Are digital wedding invitations acceptable etiquette?", "Yes. Digital invitations are widely accepted, especially for casual and modern weddings. Many couples pair them with a printed card for close family.")],
        cta_title="Ready to invite your guests?", cta_text="Pick a wedding template and share your invitation today. Design for free, pay only when you publish."),
    "birthday": dict(
        name="Birthday", crumb="Birthday invitations",
        h1="Digital birthday invitations that get the party started",
        lead="Colorful, playful or elegant. Create a birthday invitation in minutes, text it to your guests and see who is coming, all without printing a single card.",
        why_title="Why digital birthday invitations work", why_sub="Fast for you, fun for your guests.",
        why=[("zap", "Ready in minutes", "Choose a design, add the date and place, and you are done. Perfect for last-minute parties."),
             ("send", "Share anywhere", "Text it, email it or post it in a group chat. One link reaches everyone."),
             ("bell", "Reminders that help", "Guests reply quickly and you know the headcount for cake, food and party favors.")],
        steps_title="Make a birthday invitation in four steps",
        tpl_title="Birthday invitation templates", tpl_sub="Balloons, confetti, polaroids and bold party posters.",
        templates=["Balloon Bash", "Confetti Night", "Rose Polaroids", "Poster Bold"],
        wording_title="Birthday invitation wording ideas", wording_intro="A few friendly lines to get you started.",
        wording=["Sofia is turning 8! Join us for cake, games and lots of fun on Saturday, October 19 at 2:00 PM.",
                 "Let&rsquo;s celebrate! Please join us for Daniel&rsquo;s 30th birthday dinner. Reply by October 10.",
                 "It&rsquo;s a party! Bring your dancing shoes and your best smile."],
        split_title="Party details in one tap", split_text="Guests open a single page with the time, address, dress code and RSVP button. No more scrolling through group chats to find the address.",
        split_checks=["Kids, teen and adult designs", "Add a photo of the birthday star", "See who has opened the invitation", "Edit the details after you send it"],
        split_alt="Colorful digital birthday invitation on a smartphone",
        faqs=[("How do I send a digital birthday invitation?", "Publish your invitation and share the link by text, WhatsApp or email. You can also print the QR code and add it to a party sign."),
              ("Can I make a kids birthday invitation?", "Yes. Choose a playful template like Balloon Bash or Candy Party, add a photo and your party details."),
              ("Do parents need to install anything to RSVP?", "No. Guests open the link in their phone browser and reply in seconds."),
              ("What if I need to change the time or place?", "Edit your invitation and every guest sees the update at the same link.")],
        cta_title="Let&rsquo;s plan the party", cta_text="Create a birthday invitation your guests will be excited to open."),
    "baby": dict(
        name="Baby shower", crumb="Baby shower invitations",
        h1="Digital baby shower invitations, sweet and simple",
        lead="Share the details of your baby shower with a soft, beautiful invitation. Collect replies, keep the guest list organized and enjoy the day.",
        why_title="Why digital baby shower invitations make sense", why_sub="Less to organize, more to enjoy.",
        why=[("heart", "Designs that feel personal", "Add your own photos, choose gentle colors and write your own message."),
             ("users", "Easy replies for guests", "Family and friends answer with one tap and a party size."),
             ("gift", "Everything in one place", "Share the date, the place and any registry or gift notes on a single page.")],
        steps_title="Create a baby shower invitation in four steps",
        tpl_title="Baby shower invitation templates", tpl_sub="Soft pastels, stars, botanicals and playful grids.",
        templates=["Little Star", "Bento Kids", "Botanical Journal", "Peach Polaroids"],
        wording_title="Baby shower invitation wording ideas", wording_intro="Warm words for a special day.",
        wording=["Join us for a baby shower honoring Emma. Sunday, April 6 at 1:00 PM. Please reply by March 25.",
                 "A little one is on the way! Come shower the mom-to-be with love.",
                 "Oh baby! Celebrate with us as we welcome our newest arrival."],
        split_title="Gender reveals and co-ed showers too", split_text="The same tools work for gender reveal parties, sip-and-sees and couples showers. Pick a design and customize every detail.",
        split_checks=["Soft and neutral color palettes", "Add a registry or gift note", "Track replies in real time", "Share by text, email or QR code"],
        split_alt="Baby shower digital invitation with pastel colors",
        faqs=[("Can I use MyInviteQR for a gender reveal invitation?", "Yes. Choose a template you like, edit the text and share it. Many hosts use the Starry Night or Little Star designs."),
              ("How far ahead should I send baby shower invitations?", "Most hosts send them 4 to 6 weeks before the shower, with a reply-by date about a week before the event."),
              ("Can I add a registry link?", "Yes. Add text or a link anywhere on your invitation using the editor."),
              ("Is there a limit on guests?", "Essential supports up to 50 guests and Premium up to 1,000.")],
        cta_title="Start your baby shower invitation", cta_text="Choose a sweet design and share it in minutes."),
    "quince": dict(
        name="Quinceañera", crumb="Quinceañera invitations",
        h1="Digital quinceañera invitations for a celebration to remember",
        lead="Invite family and friends with an elegant digital invitation and QR code. Create it in English or Spanish, manage your guest list and track every reply.",
        why_title="Why families choose digital quinceañera invitations", why_sub="Made for large celebrations with many guests.",
        why=[("users", "Big guest lists, handled", "Premium supports up to 1,000 guests, with groups for family, friends and court members."),
             ("globe", "English and Spanish", "Create your invitation in the language your family prefers."),
             ("qr", "QR code for the venue", "Add the code to programs, menus and welcome signs so guests can find the schedule.")],
        steps_title="Create a quinceañera invitation in four steps",
        tpl_title="Quinceañera invitation templates", tpl_sub="Regal frames, romantic blooms and dreamy night skies.",
        templates=["Royal Frame", "Lavender Dream", "Cherry Blossom", "Twin Moons"],
        wording_title="Quinceañera invitation wording ideas", wording_intro="Traditional and modern options.",
        wording=["With the blessing of God and our parents, we invite you to celebrate the quincea&ntilde;era of Valentina on Saturday, August 9 at 6:00 PM.",
                 "Sweet fifteen! Join us for a night of music, dancing and family.",
                 "Con la bendici&oacute;n de Dios y de mis padres, te invito a celebrar mis quince a&ntilde;os."],
        split_title="Keep the whole family informed", split_text="Send a personal link to each guest and see who has opened it. Update the schedule at any time without reprinting anything.",
        split_checks=["Groups for family, friends and court", "Individual links for each guest (Premium)", "Export your guest list to CSV", "Up to 1,000 guests with Premium"],
        split_alt="Elegant digital quinceañera invitation on a phone",
        faqs=[("Can I make my quinceañera invitation in Spanish?", "Yes. You can write your invitation in Spanish or English, or both. The editor lets you type any text you like."),
              ("How many guests can I invite to my quinceañera?", "Premium supports up to 1,000 guests, which works for large family celebrations."),
              ("Can I also invite people to the church ceremony and the party?", "Yes. Add both the ceremony and the reception details to one invitation."),
              ("Are Sweet 16 invitations supported too?", "Absolutely. Choose any template and edit it for a Sweet 16, a debutante ball or any coming-of-age celebration.")],
        cta_title="Create your quinceañera invitation", cta_text="Choose an elegant design and share it with your family today."),
    "corporate": dict(
        name="Corporate", crumb="Corporate event invitations",
        h1="Corporate event invitations that look professional",
        lead="Invite clients, partners and teams to launches, galas, conferences and holiday parties. Clean design, online RSVP and a QR code that makes check-in and sharing easy.",
        why_title="Why teams use digital invitations for events", why_sub="Polished, trackable and quick to send.",
        why=[("brief", "A professional first impression", "Clean, modern layouts with your colors and your logo photo."),
             ("chart", "Know your headcount", "See RSVPs in real time so catering and seating are always accurate."),
             ("shield", "Control the details", "Update the agenda or the venue and everyone sees the newest version instantly.")],
        steps_title="Create an event invitation in four steps",
        tpl_title="Corporate invitation templates", tpl_sub="Modern, minimal and editorial layouts.",
        templates=["Modern Hero", "Studio Split", "Poster Noir", "Year in Review"],
        wording_title="Corporate invitation wording ideas", wording_intro="Concise, professional copy you can adapt.",
        wording=["You are invited to the Northwind Annual Summit on Thursday, March 12 at 6:00 PM. Please reply by March 1.",
                 "Join us for an evening of networking, food and inspiring talks.",
                 "The team is celebrating a great year. Please RSVP to our holiday party."],
        split_title="Built for events of every size", split_text="From a 30-person client dinner to a 1,000-guest conference, use groups, a custom link and analytics to run the guest list with confidence.",
        split_checks=["Remove MyInviteQR branding with Premium", "Custom link for your event", "Open analytics", "Export attendees to CSV"],
        split_alt="Corporate event digital invitation with QR code",
        faqs=[("Can I remove the MyInviteQR branding?", "Yes. The Premium plan removes MyInviteQR branding for a fully white-label look."),
              ("How many attendees can I invite?", "Essential supports up to 50 guests. Premium supports up to 1,000."),
              ("Can I use a QR code for event check-in?", "Every invitation has its own QR code that opens the event page. It is ideal for signs and printed materials."),
              ("Can I export the guest list?", "Yes. Export your guests and their RSVP status to a CSV file at any time.")],
        cta_title="Invite your guests in style", cta_text="Create a professional event invitation and start collecting RSVPs."),
    "qr": dict(
        name="QR code", crumb="QR code invitations",
        h1="QR code invitations guests scan to open and RSVP",
        lead="Every MyInviteQR invitation comes with its own QR code. Print it on cards and signs or show it on a screen. One scan takes guests to your event details and the RSVP button.",
        why_title="Why use a QR code on your invitation", why_sub="The fastest bridge between paper and phone.",
        why=[("qr", "One scan, zero typing", "Guests point their camera at the code and your invitation opens instantly."),
             ("phone", "Works with any phone", "Every modern iPhone and Android camera reads QR codes with no extra app."),
             ("link", "Same link, always current", "The QR code never changes. Update your details and everyone sees the latest version.")],
        steps_title="Create a QR code invitation in four steps",
        tpl_title="Templates with a QR code built in", tpl_sub="Each design has room for your QR code.",
        templates=["Garden Romance", "Boho Arch", "Balloon Bash", "Sage Circles"],
        wording_title="Where to place your QR code", wording_intro="A few smart places to put the code so guests always find it.",
        wording=["On printed save-the-dates and invitation cards: &ldquo;Scan to RSVP.&rdquo;", "On a welcome sign at the venue: &ldquo;Scan for the schedule and the map.&rdquo;", "On table cards or menus: &ldquo;Scan to share your photos.&rdquo;"],
        split_title="A QR code you can download and print", split_text="Download your QR code as a high-quality image and use it anywhere. It is included with every plan.",
        split_checks=["Included in Essential and Premium", "Sharp at any size", "Works with the invitation link", "Add it directly to your design"],
        split_alt="QR code invitation printed on a card and scanned by a phone",
        faqs=[("What is a QR code invitation?", "A QR code invitation includes a scannable code that opens your digital invitation. Guests scan it with their phone camera to see the details and RSVP."),
              ("How do I make a QR code invitation?", "Create your event in MyInviteQR, pick a template and publish. Your QR code is generated automatically and can be downloaded."),
              ("Does the QR code expire?", "The code stays valid while your invitation is active. You can add a 6-month extension for $6.99 to keep it working longer."),
              ("Can I put the QR code on printed cards?", "Yes. Download it and add it to your printed invitations, signs, menus or programs.")],
        cta_title="Create your QR code invitation", cta_text="Design it, download the code and share it anywhere."),
    "rsvp": dict(
        name="Online RSVP", crumb="Online RSVP",
        h1="Online RSVP that makes tracking guests effortless",
        lead="Stop chasing replies in group chats. Guests answer from a single link or QR code, and you see who is coming, who declined and who has not responded yet.",
        why_title="Why an online RSVP beats texts and spreadsheets", why_sub="Everything in one clean dashboard.",
        why=[("users", "Every reply in one list", "Yes, no and maybe answers with the number of people in each party."),
             ("chart", "See who opened it", "Know who has seen your invitation so you can follow up with the right people."),
             ("send", "Personal links for each guest", "Send an individual link so the guest is recognized automatically (Premium).")],
        steps_title="Start collecting RSVPs in four steps",
        tpl_title="Invitations with an RSVP button", tpl_sub="Every template includes an RSVP button you can restyle.",
        templates=["Golden Arch", "Photo Grid Party", "Magazine", "Palm Paradise"],
        wording_title="RSVP wording that gets replies", wording_intro="Short prompts that make it easy for guests to respond.",
        wording=["Kindly reply by May 1 using the button below.", "Let us know if you can make it. We would love to celebrate with you.", "Please confirm your attendance and the size of your party."],
        split_title="Import your guest list and stay organized", split_text="Upload a CSV or add guests manually. Filter by confirmed, pending, declined, maybe, opened and not opened.",
        split_checks=["Import and export CSV", "Groups and party sizes", "Filters and search", "Real-time updates"],
        split_alt="RSVP guest list dashboard with filters",
        faqs=[("How does online RSVP work?", "Guests open your invitation link, tap the RSVP button and answer yes, no or maybe with their party size. You see the response in your dashboard right away."),
              ("Do guests need an account to RSVP?", "No. They only need the link or QR code."),
              ("Can I close RSVPs after a deadline?", "You control your invitation and can update the details or the reply-by date at any time."),
              ("Can I download my guest list?", "Yes. Export your guests and their responses to CSV whenever you need to.")],
        cta_title="Get your RSVPs in one place", cta_text="Create your invitation and start collecting replies today."),
}

POSTS = {
    "how-to-write-wedding-invitation-wording": dict(
        title="Wedding Invitation Wording: Examples & Tips | MyInviteQR",
        h1="Wedding Invitation Wording: 15 Examples and Etiquette Tips",
        desc="Not sure what to write on your wedding invitation? Get modern and traditional wording examples, RSVP lines and etiquette tips for every situation.",
        keywords="wedding invitation wording, what to write on a wedding invitation, wedding invitation examples, wedding RSVP wording, digital wedding invitation wording",
        date="2026-09-20", date_h="September 20, 2026", read=6,
        body="""<p>Your wedding invitation sets the tone for your day. The right words tell guests who is hosting, when and where to show up, and how to reply. Here is how to write yours, with examples you can copy and adapt.</p>
<h2>What every wedding invitation should include</h2><ul><li>The names of the couple</li><li>A line that invites guests</li><li>The date and time</li><li>The venue and address</li><li>How and when to RSVP</li><li>Optional: dress code, website or registry</li></ul>
<h2>Traditional wording examples</h2>
<blockquote>Mr. and Mrs. James Carter request the honor of your presence at the marriage of their daughter, Emma Grace, to Jack Morgan, on Saturday, the fourteenth of June, two thousand twenty-six, at four o&rsquo;clock in the afternoon.</blockquote>
<blockquote>Together with their families, Emma Carter and Jack Morgan invite you to celebrate their marriage.</blockquote>
<h2>Modern wording examples</h2>
<blockquote>We are getting married! Join us for a celebration of love, laughter and dancing.</blockquote>
<blockquote>Two hearts, one love story. Please join us as we say &ldquo;I do.&rdquo;</blockquote>
<blockquote>Emma and Jack are tying the knot, and you are invited to the party.</blockquote>
<h2>RSVP wording</h2><ul><li>Kindly reply by May 1.</li><li>Please respond using the button below by May 1.</li><li>We can&rsquo;t wait to celebrate with you. Let us know if you can make it.</li></ul>
<h2>Tips for digital wedding invitations</h2><p>With a digital invitation you can add a map, a schedule and a registry link in one place, and guests can reply with one tap. Update details any time without reprinting. A QR code on your save-the-date or program takes guests straight to the latest version.</p>
<h2>Make it yours</h2><p>Keep your tone consistent with your event: formal for a black-tie ballroom, relaxed for a backyard celebration. Read it aloud, and if it sounds like you, it is right.</p>"""),
    "digital-vs-paper-invitations": dict(
        title="Digital vs Paper Invitations: Which Is Better? | MyInviteQR",
        h1="Digital vs. Paper Invitations: Which Is Better for Your Event?",
        desc="Compare digital and paper invitations on cost, speed, RSVPs, etiquette and environmental impact, and learn when each option makes the most sense.",
        keywords="digital vs paper invitations, are digital invitations tacky, e-invitations vs paper, cost of paper invitations, paperless invitations",
        date="2026-09-20", date_h="September 20, 2026", read=5,
        body="""<p>Choosing between digital and paper invitations comes down to your event, your budget and your guests. Here is an honest comparison.</p>
<h2>Cost</h2><p>Paper invitations add up quickly: design, printing, envelopes and postage for every guest. A digital invitation is a flat price per event, no matter how many people you invite.</p>
<h2>Speed</h2><p>Digital invitations are ready in minutes and arrive instantly by text or email. Paper takes days or weeks to design, print and mail.</p>
<h2>RSVPs</h2><p>With paper, replies come back by mail, call or text and you track them by hand. Digital invitations collect answers online and show you a live guest list.</p>
<h2>Flexibility</h2><p>If the venue or time changes, you can edit a digital invitation and everyone sees the update. A paper card has to be reprinted and resent.</p>
<h2>Etiquette</h2><p>Digital invitations are widely accepted today, especially for birthdays, baby showers, casual weddings and corporate events. For very formal occasions, many hosts send a printed card to close family and a digital invitation to everyone else.</p>
<h2>The best of both worlds</h2><p>Add a QR code to a printed card. Guests get the keepsake and you get real-time RSVPs and easy updates.</p>"""),
    "how-to-make-a-qr-code-invitation": dict(
        title="How to Make a QR Code Invitation (Step by Step) | MyInviteQR",
        h1="How to Make a QR Code Invitation in 5 Easy Steps",
        desc="Learn how to create a QR code invitation that opens your event details and RSVP page. Simple steps, design tips and where to place the code.",
        keywords="how to make a QR code invitation, QR code invitation template, QR code for wedding invitation, QR code party invitation, scan to RSVP",
        date="2026-09-20", date_h="September 20, 2026", read=5,
        body="""<p>A QR code invitation lets guests scan a code with their phone and open your event details instantly. Here is how to make one.</p>
<h2>1. Create a digital invitation</h2><p>Start by designing your invitation online. Choose a template, add the event details and customize the colors and photos.</p>
<h2>2. Add your RSVP button</h2><p>Include an RSVP button so guests can reply straight from the invitation. It is the fastest way to get an accurate headcount.</p>
<h2>3. Publish to generate your QR code</h2><p>When you publish, your invitation gets its own link and QR code. Download the code as an image.</p>
<h2>4. Place the QR code where guests will see it</h2><ul><li>Printed save-the-dates and invitation cards</li><li>Welcome signs and posters at the venue</li><li>Menus, programs and table cards</li><li>Social media posts and screens</li></ul>
<h2>5. Test before you print</h2><p>Scan the code with an iPhone and an Android phone. Make sure it is at least 0.8 inches wide when printed and has plenty of blank space around it.</p>
<h2>Design tips</h2><p>Use dark code on a light background, add a short instruction like &ldquo;Scan to RSVP&rdquo; and keep the code away from busy patterns.</p>"""),
}
