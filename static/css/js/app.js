function showStatus(
    message,
    error = false
) {

    const element =
        document.getElementById(
            "status"
        );

    if (!element) {
        return;
    }

    element.textContent =
        message;

    element.className =
        error
            ? "alert"
            : "muted";
}


function money(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(value || 0);
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => {

            const entities = {

                "&":
                    "&amp;",

                "<":
                    "&lt;",

                ">":
                    "&gt;",

                '"':
                    "&quot;",

                "'":
                    "&#039;"
            };

            return entities[
                character
            ];
        }
    );
}


function escapeAttr(value) {

    return escapeHtml(
        value
    );
}


function renderResults(data) {

    const root =
        document.getElementById(
            "results"
        );

    if (!root) {
        return;
    }

    root.classList.remove(
        "hidden"
    );


    const allocationHtml =
        Object.entries(
            data.allocations || {}
        )
        .map(
            ([key, value]) => `

                <div class="metric">

                    <span>
                        ${escapeHtml(key)}
                    </span>

                    <b>
                        ${money(value)}
                    </b>

                </div>

            `
        )
        .join("");


    const recommendationHtml =
        (data.recommendations || [])
        .map(
            item => `

                <article class="card recommendation">

                    <div>

                        <span class="pill">

                            ${escapeHtml(
                                item.category
                            )}

                        </span>

                        <h3>

                            ${escapeHtml(
                                item.name
                            )}

                        </h3>

                        <p>

                            ${escapeHtml(
                                item.reason
                            )}

                        </p>

                    </div>


                    <div class="recommend-price">

                        <b>
                            ${money(
                                item.estimated_price
                            )}
                        </b>

                        <small>

                            ${item.quantity}
                            × ·
                            ${escapeHtml(
                                item.platform
                            )}

                        </small>


                        <a
                            class="btn secondary"
                            target="_blank"
                            rel="noopener"
                            href="${escapeAttr(
                                item.url
                            )}"
                        >

                            Open search

                        </a>

                    </div>

                </article>

            `
        )
        .join("");


    const tipsHtml =
        (data.tips || [])
        .map(
            tip => `

                <li>
                    ${escapeHtml(tip)}
                </li>

            `
        )
        .join("");


    root.innerHTML = `

        <div class="result-header">

            <div>

                <p class="eyebrow">
                    AI PLAN
                </p>

                <h2>
                    ${escapeHtml(
                        data.title
                    )}
                </h2>

                <p>
                    ${escapeHtml(
                        data.summary
                    )}
                </p>

            </div>


            <div class="total">

                <span>
                    Estimated total
                </span>

                <strong>
                    ${money(
                        data.estimated_total
                    )}
                </strong>

                <small>

                    Budget:
                    ${money(data.budget)}

                    ·

                    Savings:
                    ${money(data.savings)}

                </small>

            </div>

        </div>


        <div class="grid three">

            ${allocationHtml}

        </div>


        <div class="recommendations">

            ${recommendationHtml}

        </div>


        <div class="card">

            <h3>
                Tips
            </h3>

            <ul>
                ${tipsHtml}
            </ul>

            <p class="muted">

                ${escapeHtml(
                    data.disclaimer || ""
                )}

            </p>

        </div>
    `;


    root.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


const form =
    document.getElementById(
        "planner-form"
    );


if (form) {

    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const planner =
                form.dataset.planner;


            const button =
                form.querySelector(
                    "button"
                );


            button.disabled =
                true;


            showStatus(
                "Generating your plan…"
            );


            try {

                let response;


                if (
                    planner === "jewelry"
                ) {

                    const formData =
                        new FormData(
                            form
                        );


                    response =
                        await fetch(
                            "/api/generate-jewelry",
                            {
                                method:
                                    "POST",

                                body:
                                    formData
                            }
                        );

                }

                else {

                    const formData =
                        new FormData(
                            form
                        );


                    let body;


                    if (
                        planner === "home"
                    ) {

                        const rooms =
                            String(
                                formData.get(
                                    "rooms"
                                )
                            )
                            .split(",")
                            .map(
                                value =>
                                    value.trim()
                            )
                            .filter(Boolean);


                        const items =
                            String(
                                formData.get(
                                    "items"
                                )
                            )
                            .split(",")
                            .map(
                                value =>
                                    value.trim()
                            )
                            .filter(Boolean)
                            .map(
                                raw => {

                                    const match =
                                        raw.match(
                                            /^(\d+)\s*x?\s*(.*)$/i
                                        );


                                    return {

                                        quantity:
                                            match
                                                ? Number(
                                                    match[1]
                                                )
                                                : 1,

                                        category:
                                            match
                                                ? match[2]
                                                : raw
                                    };
                                }
                            );


                        body = {

                            budget:
                                Number(
                                    formData.get(
                                        "budget"
                                    )
                                ),

                            style:
                                formData.get(
                                    "style"
                                ),

                            rooms:
                                rooms,

                            items:
                                items
                        };

                    }

                    else {

                        body =
                            Object.fromEntries(
                                formData.entries()
                            );


                        body.budget =
                            Number(
                                body.budget
                            );


                        body.guests =
                            Number(
                                body.guests
                            );
                    }


                    response =
                        await fetch(
                            `/api/generate-${planner}`,
                            {

                                method:
                                    "POST",

                                headers: {

                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        body
                                    )
                            }
                        );
                }


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Request failed."
                    );
                }


                showStatus(
                    "Plan generated successfully."
                );


                renderResults(
                    data
                );

            }

            catch (error) {

                showStatus(
                    error.message,
                    true
                );

            }

            finally {

                button.disabled =
                    false;
            }
        }
    );
}