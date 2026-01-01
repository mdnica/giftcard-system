@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET,
    )

    if event["type"] == "checkout.session.completed":
        value = 1000  # derive from product
        raw_code = f"GC-{secrets.token_hex(6).upper()}"
        code_hash = hashlib.sha256(raw_code.encode()).hexdigest()

        crud.create_giftcard(db, code_hash, value)

    return {"status": "ok"}
