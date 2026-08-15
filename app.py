import streamlit as st

from database import (
    create_tables,
    register_user,
    login_user,
    add_family_member,
    get_family_members
)


st.set_page_config(
    page_title='mosabb',
    page_icon='🛡️',
    layout='centered'
)

create_tables()


if 'user' not in st.session_state:
    st.session_state.user = None


st.title('mosabb | مسبب')

st.caption('اعرف إذا المنتج مناسب لك ولعائلتك قبل ما تستخدمه.')


if st.session_state.user is None:

    login_tab, register_tab = st.tabs([
        'تسجيل الدخول',
        'إنشاء حساب'
    ])

    with login_tab:

        st.subheader('تسجيل الدخول')

        email = st.text_input(
            'البريد الإلكتروني',
            key='login_email'
        )

        password = st.text_input(
            'كلمة المرور',
            type='password',
            key='login_password'
        )

        if st.button(
            'دخول',
            use_container_width=True
        ):

            user = login_user(email, password)

            if user:

                st.session_state.user = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }

                st.success('تم تسجيل الدخول')

                st.rerun()

            else:

                st.error(
                    'البريد الإلكتروني أو كلمة المرور غير صحيحة'
                )


    with register_tab:

        st.subheader('إنشاء حساب عائلة')

        name = st.text_input(
            'اسمك',
            key='register_name'
        )

        email = st.text_input(
            'البريد الإلكتروني',
            key='register_email'
        )

        password = st.text_input(
            'كلمة المرور',
            type='password',
            key='register_password'
        )

        if st.button(
            'إنشاء الحساب',
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning('عب البيانات كلها')

            else:

                success = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        'تم إنشاء الحساب. الحين سجل دخولك.'
                    )

                else:

                    st.error(
                        'هذا البريد الإلكتروني مسجل من قبل'
                    )


else:

    user = st.session_state.user

    st.success(
        f'أهلاً {user["name"]} 👋'
    )

    if st.button('تسجيل الخروج'):

        st.session_state.user = None

        st.rerun()


    st.divider()

    scan_tab, family_tab = st.tabs([
        '📷 فحص منتج',
        '👨‍👩‍👧‍👦 عائلتي'
    ])


    with scan_tab:

        st.header('فحص منتج')

        st.info(
            'قريباً: صور المنتج وmosabb بيقارنه '
            'بحساسيات كل أفراد العائلة.'
        )

        picture = st.camera_input(
            'صور مكونات المنتج'
        )

        uploaded_file = st.file_uploader(
            'أو ارفع صورة',
            type=['jpg', 'jpeg', 'png']
        )


    with family_tab:

        st.header('أفراد العائلة')

        family = get_family_members(
            user['id']
        )

        if family:

            for member in family:

                with st.container(border=True):

                    st.subheader(
                        member['name']
                    )

                    st.write(
                        f'الصفة: {member["relation"]}'
                    )

                    if member['allergies']:

                        st.write(
                            'الحساسيات: '
                            + ', '.join(
                                member['allergies']
                            )
                        )

                    else:

                        st.write(
                            'لا توجد حساسيات مسجلة'
                        )

        else:

            st.info(
                'ما أضفت أحد للعائلة للحين.'
            )


        st.divider()

        st.subheader('إضافة فرد للعائلة')

        member_name = st.text_input(
            'الاسم'
        )

        relation = st.selectbox(
            'صلة القرابة',
            [
                'ابن',
                'ابنة',
                'أم',
                'أب',
                'أخ',
                'أخت',
                'أخرى'
            ]
        )

        allergies = st.multiselect(
            'الحساسيات',
            [
                'Milk / Dairy',
                'Peanuts',
                'Sesame',
                'Eggs',
                'Tree Nuts'
            ]
        )

        if st.button(
            'إضافة فرد',
            use_container_width=True
        ):

            if not member_name:

                st.warning(
                    'اكتب اسم الشخص'
                )

            elif not allergies:

                st.warning(
                    'اختر حساسية واحدة على الأقل'
                )

            else:

                add_family_member(
                    user['id'],
                    member_name,
                    relation,
                    allergies
                )

                st.success(
                    f'تمت إضافة {member_name}'
                )

                st.rerun()
