import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def create_robust_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=10, leading=14))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=14, spaceAfter=12))
    
    Story = []

    Story.append(Spacer(1, 200))
    Story.append(Paragraph("CHAI POINT ENTERPRISE OPERATIONS MANUAL", styles["Title"]))
    Story.append(Paragraph("Comprehensive Policy, Menu & SOP Guide 2025", styles["Heading2"]))
    Story.append(Paragraph("Version 4.2.0 | Confidential", styles["Center"]))
    Story.append(PageBreak())

    def add_chapter_title(title):
        Story.append(Paragraph(title, styles["Heading1"]))
        Story.append(Spacer(1, 12))

    add_chapter_title("1. Master Menu & Pricing Guide")
    Story.append(Paragraph("Detailed breakdown of all beverages, food items, ingredients, and pricing variants.", styles["Justify"]))
    Story.append(Spacer(1, 12))

    categories = {
        "Hot Teas (Chai)": ["Masala Chai", "Ginger Chai", "Elaichi Chai", "Lemon Tea", "Green Tea", "Kashmiri Kahwa", "Tulsi Tea", "Assam Strong"],
        "Hot Coffees": ["Filter Coffee", "Cappuccino", "Latte", "Espresso", "Americano", "Mocha", "Macchiato", "Flat White"],
        "Cold Beverages": ["Iced Chai", "Cold Coffee", "Vietnamese Cold Brew", "Lemon Iced Tea", "Peach Iced Tea", "Mango Lassi", "Rose Lassi", "Buttermilk"],
        "Food & Snacks": ["Bun Maska", "Samosa", "Vada Pav", "Poha", "Upma", "Banana Cake", "Chocolate Muffin", "Paneer Puff", "Chicken Puff", "Sandwich"]
    }
    
    all_items_data = []

    for category, items in categories.items():
        Story.append(Paragraph(f"1.{list(categories.keys()).index(category)+1} {category}", styles["Heading2"]))
        
        data = [["Item Name", "Description", "Small\n(INR)", "Medium\n(INR)", "Large\n(INR)", "Cals\n(kcal)"]]
        
        for item in items:
            desc = f"Premium {item} prepared with high-quality ingredients. "
            if "Chai" in item:
                desc += "Brewed with fresh tea leaves and spices."
            elif "Coffee" in item:
                desc += "Made from 100% Arabica beans."
            else:
                desc += "Freshly prepared daily."
            
            base_price = random.randint(50, 150)
            s_price, m_price, l_price = base_price, base_price + 40, base_price + 80
            cals = random.randint(100, 400)
            
            all_items_data.append({
                "name": item,
                "small": s_price,
                "medium": m_price,
                "large": l_price,
                "cals": cals
            })

            row = [
                Paragraph(f"<b>{item}</b>", styles["BodyText"]),
                Paragraph(desc, styles["BodyText"]),
                f"{s_price}",
                f"{m_price}",
                f"{l_price}",
                f"{cals}"
            ]
            data.append(row)
            
            variants = ["Sugar Free", "Jaggery", "Almond Milk", "Oat Milk", "Soy Milk"]
            for v in variants:
                v_price = base_price + (30 if "Milk" in v else 10)
                data.append([
                    Paragraph(f"  - w/ {v}", styles["BodyText"]), 
                    Paragraph("Variant option", styles["BodyText"]), 
                    f"{v_price}", 
                    f"{v_price+40}", 
                    f"{v_price+80}", 
                    "-"
                ])

        t = Table(data, colWidths=[100, 190, 55, 55, 55, 55], repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkslategrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ]))
        Story.append(t)
        Story.append(Spacer(1, 20))
    
    Story.append(PageBreak())

    add_chapter_title("2. Store Timings & Operational Schedules")
    Story.append(Paragraph("Standard operating hours for all Tier-1 and Tier-2 city outlets.", styles["Justify"]))
    
    timings_data = [["Day Type", "Opening Time", "Closing Time", "Break/Cleaning Schedule", "Notes"]]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Public Holidays"]
    
    for day in days:
        open_time = "07:00 AM" if day != "Sunday" else "08:00 AM"
        close_time = "11:00 PM" if day in ["Friday", "Saturday"] else "10:00 PM"
        row = [day, open_time, close_time, "02:00 PM - 02:30 PM", "Peak hours: 08-10 AM, 05-07 PM"]
        timings_data.append(row)
    
    t = Table(timings_data, colWidths=[80, 70, 70, 130, 150])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black), 
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("Holiday Calendar 2025 (Store Closures & Special Hours)", styles["Heading3"]))
    holidays = ["Republic Day", "Holi", "Gudi Padwa", "Eid-ul-Fitr", "Independence Day", "Ganesh Chaturthi", "Gandhi Jayanti", "Dussehra", "Diwali", "Christmas"]
    for h in holidays:
        Story.append(Paragraph(f"• {h}: Open (Special Hours: 10:00 AM - 08:00 PM)", styles["Justify"]))
    
    Story.append(PageBreak())
    
    # Load Store Data
    import json
    with open("data/stores.json", "r") as f:
        stores_data = json.load(f)

    add_chapter_title("3. Store Locations & Contact Details")
    Story.append(Paragraph("Directory of all Velvet Brew outlets across India.", styles["Justify"]))
    Story.append(Spacer(1, 12))
    
    loc_table_data = [["Store Name", "City", "Address", "Phone"]]
    
    for store in stores_data:
        # Extract City from address (simple split)
        city = store["location"]["address"].split(",")[-2].strip()
        row = [
            Paragraph(store["name"], styles["BodyText"]),
            city,
            Paragraph(store["location"]["address"], styles["BodyText"]),
            f"+91-{random.randint(70000, 99999)}-{random.randint(10000, 99999)}"
        ]
        loc_table_data.append(row)
        
    t = Table(loc_table_data, colWidths=[120, 80, 200, 100], repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    Story.append(t)
    Story.append(PageBreak())

    add_chapter_title("4. Order Fulfillment, Delivery & Cancellation Policies")
    
    policies = [
        ("Delivery Partners", "We partner with Swiggy, Zomato, and Dunzo. All orders must be handed over within 7 minutes of preparation."),
        ("Packaging Standards", "Hot beverages must be sealed with spill-proof tape. Cold beverages require double-lidding. Food items must be in grease-proof paper."),
        ("Cancellation Policy", "Orders can be cancelled by the customer within 60 seconds of placing. After 60 seconds, 100% cancellation fee applies."),
        ("Refunds", "Refunds for missing items are processed instantly via the POS. Quality complaints require a photo evidence uploaded to the merchant portal."),
        ("Late Delivery", "If an order is delayed by >45 mins, the customer is eligible for a 50% coupon for the next order.")
    ]
    
    for title, text in policies:
        Story.append(Paragraph(title, styles["Heading2"]))
        Story.append(Paragraph(text, styles["Justify"]))
        Story.append(Paragraph("Compliance with this policy is mandatory. Failure to adhere may result in penalties. " * 5, styles["Justify"]))
        Story.append(Spacer(1, 10))
    
    Story.append(PageBreak())

    add_chapter_title("4. Active Offers, Coupons & Loyalty Logic")
    
    offers_data = [["Coupon Code", "Discount", "Min Order", "Max Discount", "Validity", "Terms"]]
    for i in range(50):
        code = f"CHAI{random.randint(10,99)}"
        disc = random.choice(["10%", "20%", "Flat Rs. 50", "Flat Rs. 100", "BOGO"])
        row = [
            code, 
            disc, 
            f"Rs. {random.choice([100, 200, 300])}", 
            f"Rs. {random.choice([50, 100, 150])}", 
            "31-Dec-2025", 
            "Not valid on combos"
        ]
        offers_data.append(row)
    
    t = Table(offers_data, repeatRows=1, colWidths=[70, 70, 70, 70, 80, 140])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    Story.append(t)
    
    Story.append(PageBreak())

    add_chapter_title("5. Food Safety, Hygiene & Sanitation SOPs")
    
    sops = [
        "Hand Washing Protocol: Every 30 minutes for 20 seconds.",
        "Surface Sanitization: Tables must be wiped with disinfectant after every customer.",
        "Temperature Checks: Fridge temperature must be logged every 4 hours.",
        "Mask Policy: All staff must wear N95 masks in the kitchen area.",
        "Pest Control: Weekly fumigation is mandatory on Tuesday nights.",
        "Hair Nets: Mandatory for all kitchen and counter staff."
    ]
    
    for sop in sops:
        Story.append(Paragraph(f"• {sop}", styles["Justify"]))
        Story.append(Paragraph("Detailed Procedure: Step 1. Gather materials. Step 2. Execute task. Step 3. Log in register. Step 4. Supervisor review. " * 3, styles["Justify"]))
        Story.append(Spacer(1, 10))

    Story.append(PageBreak())

    add_chapter_title("6. Frequently Asked Questions (Knowledge Base)")
    
    faqs = [
        ("Is seating available?", "Yes, all our outlets have seating for at least 10-15 people. We follow a first-come-first-serve policy."),
        ("Do you have Wi-Fi?", "Yes, free high-speed Wi-Fi is available. SSID: ChaiPoint_Guest, Password: chai_lover."),
        ("Do you have vegan options?", "Yes, we offer Almond, Oat, and Soy milk alternatives for all beverages."),
        ("Is parking available?", "Parking availability depends on the specific outlet location. Mall outlets have parking; street outlets may not."),
        ("Do you accept UPI?", "Yes, we accept Google Pay, PhonePe, Paytm, and all UPI apps."),
        ("Can I host a meeting here?", "Yes, small meetings are welcome. Please limit laptop usage to 90 minutes during peak hours."),
        ("Do you serve sugar-free drinks?", "Yes, we can prepare any tea or coffee without sugar, or with Stevia/Jaggery."),
        ("What is the calorie count of a Samosa?", "A standard Samosa is approximately 250 kcal."),
        ("Do you deliver to offices?", "Yes, we have a corporate bulk order program. Contact B2B sales for details.")
    ]
    
    for i in range(5): 
        for q, a in faqs:
            Story.append(Paragraph(f"Q: {q}", styles["Heading3"]))
            Story.append(Paragraph(f"A: {a}", styles["Justify"]))
            Story.append(Spacer(1, 6))

    Story.append(PageBreak())
    add_chapter_title("7. Quick Reference Price List")
    Story.append(Paragraph("Compact list for quick billing reference. (Item: Small | Medium | Large)", styles["Justify"]))
    Story.append(Spacer(1, 12))
    
    for item in all_items_data:
        text = f"<b>{item['name']}</b>: Small Rs.{item['small']} | Medium Rs.{item['medium']} | Large Rs.{item['large']} | {item['cals']} kcal"
        Story.append(Paragraph(text, styles["Justify"]))
        Story.append(Spacer(1, 6))

    doc.build(Story)

if __name__ == "__main__":
    create_robust_pdf("data/store_policies.pdf")
    print("Generated Robust PDF at data/store_policies.pdf")
